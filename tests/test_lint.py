#!/usr/bin/env python3
"""Tests for engram-lint checks."""

import os
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "lib"))
from layers import ALL_LAYERS  # noqa: E402


def make_memory(tmp: str) -> Path:
    memory = Path(tmp) / ".claude" / "memory"
    for layer in ALL_LAYERS:
        (memory / layer).mkdir(parents=True, exist_ok=True)
    return memory


def run_lint(cwd: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(ROOT / "bin" / "engram-lint"), "--json"],
        capture_output=True, text=True, cwd=cwd,
    )


def test_relative_links_are_resolved_against_the_linking_file():
    """A relative link to a file that exists must not be reported as missing.

    Regression: links were resolved against the process CWD, so every relative
    link looked broken regardless of where it pointed.
    """
    with tempfile.TemporaryDirectory() as tmp:
        memory = make_memory(tmp)
        (memory / "procedural" / "run-a-decision.md").write_text(
            "# Run a Decision\n\nStart with [Reversibility](reversibility-test.md).\n"
        )
        (memory / "procedural" / "reversibility-test.md").write_text(
            "# Reversibility Test\n\nOne-way or two-way door.\n"
        )

        result = run_lint(tmp)
        assert result.returncode in (0, 1), result.stderr
        assert "reversibility" not in _missing_topics(result.stdout), \
            "an existing relative link was reported as an undocumented topic"
        print("  PASS: relative links resolve against the linking file")


def test_genuinely_broken_link_is_still_reported():
    """The check must still catch a link to a file that does not exist."""
    with tempfile.TemporaryDirectory() as tmp:
        memory = make_memory(tmp)
        (memory / "procedural" / "a.md").write_text(
            "# A\n\nSee [Nowhere](does-not-exist.md).\n"
        )
        result = run_lint(tmp)
        topics = _missing_topics(result.stdout)
        assert "nowhere" in topics, f"broken link not reported; got {topics}"
        print("  PASS: a genuinely broken link is still reported")


def test_external_links_are_ignored():
    """http(s) links are not memory pages and must not be flagged."""
    with tempfile.TemporaryDirectory() as tmp:
        memory = make_memory(tmp)
        (memory / "procedural" / "a.md").write_text(
            "# A\n\nSee [Upstream](https://example.com/guide.md).\n"
        )
        result = run_lint(tmp)
        topics = _missing_topics(result.stdout)
        assert "upstream" not in topics, f"external link flagged; got {topics}"
        print("  PASS: external links are ignored")


def _missing_topics(stdout: str) -> list:
    """The topics engram-lint reported as referenced but undocumented."""
    import json
    try:
        data = json.loads(stdout)
    except json.JSONDecodeError:
        return []
    return [
        i.get("topic", "").lower()
        for i in data.get("issues", [])
        if i.get("type") == "missing"
    ]


if __name__ == "__main__":
    print("Running engram-lint tests...\n")

    test_relative_links_are_resolved_against_the_linking_file()
    test_genuinely_broken_link_is_still_reported()
    test_external_links_are_ignored()

    print("\nAll tests passed!")
