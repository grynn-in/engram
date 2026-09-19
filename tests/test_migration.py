#!/usr/bin/env python3
"""Upgrade path: a project initialised by an older engram must end up current.

Before this landed, `engram init` saw an existing "## Engram" heading and
skipped. The new layer directories were created and CLAUDE.md was never
updated, so Claude was never told the layers existed and they stayed empty.
"""

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).parent.parent
BIN = ROOT / "bin"
sys.path.insert(0, str(ROOT / "lib"))
from layers import ALL_LAYERS, LAYER_COUNT, PROTOCOL_END, PROTOCOL_START  # noqa: E402

# A CLAUDE.md exactly as an older engram wrote it: no fences, 5 layers.
LEGACY_CLAUDE_MD = """\
# Project — Claude Code Reference

## Engram — 5-Layer Memory System

You have a 5-layer memory system in `.claude/memory/`:

| Layer | Path | Purpose |
|-------|------|---------|
| 1. Core Identity | `CLAUDE.md` | Permanent rules, always active |
| 2. Lossless | `memory/lossless/` | Raw session transcripts (append-only) |
| 3. Semantic | `memory/semantic/` | Distilled facts, searchable knowledge |
| 4. Procedural | `memory/procedural/` | Workflows, standards, how-tos |
| 5. Active | `memory/active/` | Today's tasks, context, blockers |

**Retrieval priority**: Active → Semantic → Procedural → Lossless

## House Rules

Project-specific content that must survive the upgrade.
"""


def make_legacy_project(tmp: str) -> Path:
    root = Path(tmp)
    memory = root / ".claude" / "memory"
    for layer in ("active", "semantic", "procedural", "lossless"):
        (memory / layer).mkdir(parents=True)
    (memory / "active" / "current-tasks.md").write_text("# Current Tasks\n")
    # The schema an older engram shipped, taken from git history via the
    # digest list; any listed digest counts as unmodified.
    shutil.copy(ROOT / "templates" / "default" / "schema.md", memory / "schema.md")
    (root / "CLAUDE.md").write_text(LEGACY_CLAUDE_MD)
    return root


def run_init(cwd: str):
    # Pin ENGRAM_HOME to this checkout so the test never picks up whatever
    # version happens to be installed on the machine running it.
    import os
    env = dict(os.environ, ENGRAM_HOME=str(ROOT))
    return subprocess.run(["bash", str(BIN / "engram-init"), cwd],
                          capture_output=True, text=True, cwd=cwd, env=env)


def test_legacy_project_is_brought_current():
    with tempfile.TemporaryDirectory() as tmp:
        root = make_legacy_project(tmp)
        result = run_init(tmp)
        assert result.returncode == 0, result.stderr

        for layer in ALL_LAYERS:
            assert (root / ".claude" / "memory" / layer).is_dir(), f"{layer}/ missing"

        content = (root / "CLAUDE.md").read_text()
        assert "5-Layer" not in content, "stale layer count left in CLAUDE.md"
        assert f"{LAYER_COUNT}-Layer" in content, "protocol was not refreshed"
        for layer in ALL_LAYERS:
            assert f"`memory/{layer}/`" in content, f"{layer}/ missing from protocol table"
        print("  PASS: a legacy project is brought fully current")


def test_project_content_survives():
    with tempfile.TemporaryDirectory() as tmp:
        root = make_legacy_project(tmp)
        run_init(tmp)
        content = (root / "CLAUDE.md").read_text()
        assert "## House Rules" in content, "project section was destroyed"
        assert "must survive the upgrade" in content
        print("  PASS: project-specific content survives the upgrade")


def test_upgrade_matches_a_fresh_install():
    with tempfile.TemporaryDirectory() as old, tempfile.TemporaryDirectory() as new:
        make_legacy_project(old)
        run_init(old)
        run_init(new)

        def fenced(p):
            t = (Path(p) / "CLAUDE.md").read_text()
            return t[t.index(PROTOCOL_START):t.index(PROTOCOL_END)]

        assert fenced(old) == fenced(new), "upgraded protocol differs from a fresh one"
        assert (Path(old) / ".claude/memory/schema.md").read_text() == \
               (Path(new) / ".claude/memory/schema.md").read_text(), "schema.md not refreshed"
        print("  PASS: an upgraded project matches a fresh install")


def test_upgrade_is_idempotent():
    with tempfile.TemporaryDirectory() as tmp:
        root = make_legacy_project(tmp)
        run_init(tmp)
        once = (root / "CLAUDE.md").read_text()
        run_init(tmp)
        run_init(tmp)
        twice = (root / "CLAUDE.md").read_text()
        assert once == twice, "repeat init changed the file"
        assert twice.count(PROTOCOL_START) == 1, "protocol block was duplicated"
        print("  PASS: repeated init is idempotent")


def test_edited_schema_is_never_overwritten():
    with tempfile.TemporaryDirectory() as tmp:
        root = make_legacy_project(tmp)
        schema = root / ".claude" / "memory" / "schema.md"
        schema.write_text(schema.read_text() + "\n## Our house rule\n\nAll facts cite a ticket.\n")
        run_init(tmp)
        assert "Our house rule" in schema.read_text(), "an edited schema.md was clobbered"
        print("  PASS: an edited schema.md is left alone")


def test_shipped_schema_digest_is_listed():
    """The current schema.md must be in the digest list, or upgrades break."""
    from layers import schema_digest
    shipped = ROOT / "templates" / "default" / "schema.md"
    listed = (ROOT / "templates" / "default" / "schema.known-digests").read_text()
    digest = schema_digest(shipped)
    assert digest in listed, (
        "templates/default/schema.md changed without appending its digest to "
        "templates/default/schema.known-digests — existing projects will be "
        f"told their schema 'looks edited' and never upgraded.\n  add: {digest}"
    )
    print("  PASS: the shipped schema digest is listed")


if __name__ == "__main__":
    print("Running upgrade-path tests...\n")
    test_legacy_project_is_brought_current()
    test_project_content_survives()
    test_upgrade_matches_a_fresh_install()
    test_upgrade_is_idempotent()
    test_edited_schema_is_never_overwritten()
    test_shipped_schema_digest_is_listed()
    print("\nAll tests passed!")
