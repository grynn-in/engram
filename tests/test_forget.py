#!/usr/bin/env python3
"""End-to-end guarantee for `engram forget`.

forget exists so that superseded knowledge stops coming back. Before the
.archive exclusion landed, a forgotten file was still walked by every command:
it returned as the TOP search hit, outranking the live knowledge that replaced
it, and xref wrote links to it into other files.
"""

import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).parent.parent
BIN = ROOT / "bin"


def seed(tmp: str) -> Path:
    subprocess.run(["bash", str(BIN / "engram-init"), tmp],
                   capture_output=True, text=True, cwd=tmp, check=True)
    memory = Path(tmp) / ".claude" / "memory"
    (memory / "semantic" / "auth-notes.md").write_text(
        "# Auth notes\n\nJWT expiry is 900 seconds as of 2026-01-01.\n")
    (memory / "semantic" / "deploy-runbook.md").write_text(
        "# Deployment runbook\n\nBlue-green deploy via the release script.\n")
    return memory


def search(tmp: str, query: str) -> str:
    return subprocess.run(
        [sys.executable, str(BIN / "engram-search"), query],
        capture_output=True, text=True, cwd=tmp,
    ).stdout


def test_forget_removes_content_from_search():
    with tempfile.TemporaryDirectory() as tmp:
        seed(tmp)
        assert "auth-notes.md" in search(tmp, "JWT expiry"), \
            "precondition failed: the file should be findable before forget"

        subprocess.run([sys.executable, str(BIN / "engram-forget"), "JWT expiry"],
                       capture_output=True, text=True, cwd=tmp)

        after = search(tmp, "JWT expiry")
        assert "auth-notes.md" not in after, \
            "a superseded file still appears in search results:\n" + after
        print("  PASS: forgotten content no longer surfaces in search")


def test_forget_preserves_the_file():
    """Governance rule: never delete — supersede."""
    with tempfile.TemporaryDirectory() as tmp:
        memory = seed(tmp)
        subprocess.run([sys.executable, str(BIN / "engram-forget"), "JWT expiry"],
                       capture_output=True, text=True, cwd=tmp)

        archived = memory / "semantic" / ".archive" / "auth-notes.md"
        assert archived.is_file(), "forget must archive, not delete"
        assert "JWT expiry" in archived.read_text(), "archived content was lost"
        assert not (memory / "semantic" / "auth-notes.md").exists(), \
            "the live copy should have moved"
        print("  PASS: forget archives rather than deletes")


def test_live_knowledge_is_untouched():
    with tempfile.TemporaryDirectory() as tmp:
        memory = seed(tmp)
        subprocess.run([sys.executable, str(BIN / "engram-forget"), "JWT expiry"],
                       capture_output=True, text=True, cwd=tmp)
        assert (memory / "semantic" / "deploy-runbook.md").is_file(), \
            "forget removed an unrelated file"
        print("  PASS: unrelated knowledge is untouched")


def test_lint_ignores_archived_files():
    with tempfile.TemporaryDirectory() as tmp:
        seed(tmp)
        subprocess.run([sys.executable, str(BIN / "engram-forget"), "JWT expiry"],
                       capture_output=True, text=True, cwd=tmp)
        out = subprocess.run(
            [sys.executable, str(BIN / "engram-lint"), "--json"],
            capture_output=True, text=True, cwd=tmp,
        ).stdout
        import json
        try:
            issues = json.loads(out).get("issues", [])
        except json.JSONDecodeError:
            issues = []
        offenders = [i.get("file", "") for i in issues if ".archive" in i.get("file", "")]
        assert not offenders, f"lint reported archived files: {offenders}"
        print("  PASS: lint does not scan archived files")


if __name__ == "__main__":
    print("Running engram-forget tests...\n")
    test_forget_removes_content_from_search()
    test_forget_preserves_the_file()
    test_live_knowledge_is_untouched()
    test_lint_ignores_archived_files()
    print("\nAll tests passed!")
