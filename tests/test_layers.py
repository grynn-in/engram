#!/usr/bin/env python3
"""Tests for the layer registry (lib/layers.py) and its consumers.

The point of these tests is that adding a layer should be a one-line change in
lib/layers.py. The drift tests below fail loudly if a layer name gets hardcoded
somewhere again, or if a generated file stops matching its generator.
"""

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "lib"))

from layers import (  # noqa: E402
    ALL_LAYERS,
    APPEND_ONLY_LAYERS,
    BY_NAME,
    CURATED_LAYERS,
    DOC_ORDER,
    LAYER_COUNT,
    LAYERS,
    SEARCHABLE_LAYERS,
    SETS,
    SKIP_DIRS,
    SHARED_LAYERS,
    TRANSFERABLE_LAYERS,
    is_skipped,
    layer_of,
    layer_set,
    protocol_block,
    search_bonus,
)


def test_registry_is_coherent():
    names = [l.name for l in LAYERS]
    assert len(names) == len(set(names)), "duplicate layer name"
    assert LAYER_COUNT == len(LAYERS) + 1, "CLAUDE.md is layer 1"

    ranks = sorted(l.doc_rank for l in LAYERS)
    assert ranks == list(range(2, len(LAYERS) + 2)), f"doc_rank must be contiguous: {ranks}"
    assert [l.name for l in DOC_ORDER][-1] == "active", "active is the last numbered layer"

    for name, members in SETS.items():
        assert set(members) <= set(ALL_LAYERS), f"set {name} has a non-layer member"
        assert len(members) == len(set(members)), f"set {name} has duplicates"

    print("  PASS: registry is coherent")


def test_new_layers_present():
    for name in ("traps", "vision"):
        assert name in ALL_LAYERS, f"{name} missing from the registry"
        layer = BY_NAME[name]
        assert layer.curated, f"{name} should be curated knowledge"
        assert layer.transferable, f"{name} should travel with sync/export/templates"
        assert not layer.append_only
        assert name in CURATED_LAYERS
        assert name in TRANSFERABLE_LAYERS
        assert name in SEARCHABLE_LAYERS
        assert name in SHARED_LAYERS

    assert BY_NAME["traps"].search_bonus > BY_NAME["semantic"].search_bonus, \
        "a trap is the most expensive knowledge to re-learn; it should outrank facts"
    print("  PASS: traps/ and vision/ are registered and transferable")


def test_set_semantics():
    assert APPEND_ONLY_LAYERS == ["lossless"]
    assert set(SEARCHABLE_LAYERS) == set(ALL_LAYERS) - set(APPEND_ONLY_LAYERS)
    assert "lossless" not in TRANSFERABLE_LAYERS, "raw history should not sync by default"
    assert "active" not in TRANSFERABLE_LAYERS, "today's tasks are project-local"

    try:
        layer_set("nope")
    except KeyError as exc:
        assert "unknown layer set" in exc.args[0]
    else:
        raise AssertionError("unknown set should raise, not fall back silently")
    print("  PASS: set semantics hold")


def test_skip_dirs_cover_cache_and_archive():
    """Every memory walk must skip these; .archive is what makes forget work."""
    assert {".cache", ".archive"} <= set(SKIP_DIRS)
    assert is_skipped("memory/semantic/.archive/old.md")
    assert is_skipped("memory/.cache/embeddings.json")
    assert is_skipped("memory/lossless/.archive/2026-01/a.md")
    assert not is_skipped("memory/semantic/live.md")
    assert not is_skipped("memory/traps/archive-strategy.md"), \
        "a filename merely containing 'archive' must not be skipped"
    print("  PASS: skip dirs cover .cache and .archive")


def test_path_lookup_and_scoring():
    assert layer_of("/x/.claude/memory/traps/qdrant-silent.md") == "traps"
    assert layer_of("/x/.claude/memory/vision/no-cloud.md") == "vision"
    assert layer_of("/x/somewhere/else/readme.md") is None
    assert search_bonus("/x/.claude/memory/traps/a.md") == BY_NAME["traps"].search_bonus
    assert search_bonus("/x/outside/a.md") == 0.0
    # Windows-style separators must resolve too.
    assert layer_of(r"C:\\proj\\.claude\\memory\\vision\\a.md") == "vision"
    print("  PASS: path lookup and scoring work")


def test_protocol_block_covers_every_layer():
    block = protocol_block()
    assert f"{LAYER_COUNT}-Layer" in block
    for layer in LAYERS:
        assert f"`memory/{layer.name}/`" in block, f"{layer.name} missing from protocol table"
    for layer in LAYERS:
        if layer.curated or layer.name == "active":
            assert layer.writes in block, f"{layer.name} has no update rule in the protocol"
    print("  PASS: protocol block covers every layer")


def test_generated_snippets_match_generator():
    """Every claude.md.snippet is generated as protocol_block() + claude.md.extra."""
    block = protocol_block()
    checked = 0
    for tpl in sorted((ROOT / "templates").iterdir()):
        snippet = tpl / "claude.md.snippet"
        if not snippet.is_file():
            continue
        extra = tpl / "claude.md.extra"
        expected = block + ("\n" + extra.read_text() if extra.is_file() else "")
        assert snippet.read_text() == expected, (
            f"templates/{tpl.name}/claude.md.snippet is stale.\n"
            f"It must equal `python3 lib/layers.py --protocol`"
            + (f" followed by templates/{tpl.name}/claude.md.extra" if extra.is_file() else "")
        )
        checked += 1
    assert checked >= 2, "expected at least the default and product snippets"
    print(f"  PASS: {checked} generated snippets match the registry")


def test_template_extra_has_no_protocol_block():
    """claude.md.extra holds only template-specific guidance, never the protocol."""
    for tpl in sorted((ROOT / "templates").iterdir()):
        extra = tpl / "claude.md.extra"
        if extra.is_file():
            text = extra.read_text()
            assert "## Engram" not in text, (
                f"templates/{tpl.name}/claude.md.extra duplicates the protocol block; "
                "it is generated and must not be copied"
            )
    print("  PASS: no template duplicates the protocol block")


def test_no_hardcoded_layer_lists_in_commands():
    """No command may re-list the layers itself — that is what the registry is for."""
    names = "|".join(sorted(BY_NAME))
    # A python literal listing two or more layer names: ["semantic", "procedural"]
    py_literal = re.compile(
        r"[\[\(\{]\s*[\"']("
        + names
        + r")[\"']\s*,\s*[\"']("
        + names
        + r")[\"']"
    )
    # A bash loop listing them bare: for layer in semantic procedural; do
    sh_loop = re.compile(
        r"for\s+\w+\s+in\s+(?:(?:" + names + r")\s+)+(?:" + names + r")\s*;"
    )

    offenders = []
    for path in sorted((ROOT / "bin").iterdir()):
        if not path.is_file():
            continue
        for i, line in enumerate(path.read_text(errors="ignore").splitlines(), 1):
            if py_literal.search(line) or sh_loop.search(line):
                offenders.append(f"{path.name}:{i}: {line.strip()}")

    assert not offenders, "layer names hardcoded outside lib/layers.py:\n  " + "\n  ".join(offenders)
    print("  PASS: no command hardcodes a layer list")


def test_bash_shim_agrees_with_python():
    """lib/layers.sh must report exactly what lib/layers.py reports."""
    for name in SETS:
        out = subprocess.run(
            ["bash", "-c", f'source "{ROOT}/lib/layers.sh"; engram_layers {name}'],
            capture_output=True, text=True,
        )
        assert out.returncode == 0, f"{name}: {out.stderr}"
        assert out.stdout.split() == layer_set(name), f"bash/python disagree on set {name}"

    bad = subprocess.run(
        ["bash", "-c", f'source "{ROOT}/lib/layers.sh"; engram_layers bogus'],
        capture_output=True, text=True,
    )
    assert bad.returncode != 0, "an unknown set must fail loudly in bash too"
    print("  PASS: bash shim agrees with the python registry")


if __name__ == "__main__":
    print("Running layer registry tests...\n")

    test_registry_is_coherent()
    test_new_layers_present()
    test_set_semantics()
    test_skip_dirs_cover_cache_and_archive()
    test_path_lookup_and_scoring()
    test_protocol_block_covers_every_layer()
    test_generated_snippets_match_generator()
    test_template_extra_has_no_protocol_block()
    test_no_hardcoded_layer_lists_in_commands()
    test_bash_shim_agrees_with_python()

    print("\nAll tests passed!")
