#!/usr/bin/env python3
"""Every place that declares engram's version must agree.

They had already drifted three ways: bin/engram said 0.7.0, pyproject.toml and
npm/package.json said 0.6.0, and the Homebrew formula pinned a v0.7.0 tarball.
"""

import json
import re
from pathlib import Path

ROOT = Path(__file__).parent.parent


def cli_version() -> str:
    m = re.search(r'^VERSION="([^"]+)"', (ROOT / "bin" / "engram").read_text(), re.MULTILINE)
    assert m, "bin/engram has no VERSION"
    return m.group(1)


def test_all_declared_versions_agree():
    expected = cli_version()
    found = {"bin/engram": expected}

    m = re.search(r'^version = "([^"]+)"', (ROOT / "pyproject.toml").read_text(), re.MULTILINE)
    assert m, "pyproject.toml has no version"
    found["pyproject.toml"] = m.group(1)

    pkg = ROOT / "npm" / "package.json"
    if pkg.is_file():
        found["npm/package.json"] = json.loads(pkg.read_text())["version"]

    formula = ROOT / "Formula" / "engram.rb"
    if formula.is_file():
        m = re.search(r"/v([0-9]+\.[0-9]+\.[0-9]+)\.tar\.gz", formula.read_text())
        assert m, "Formula/engram.rb has no versioned tarball url"
        found["Formula/engram.rb"] = m.group(1)

    mismatched = {k: v for k, v in found.items() if v != expected}
    assert not mismatched, (
        f"version drift — bin/engram says {expected}, but: {mismatched}"
    )
    print(f"  PASS: all {len(found)} version declarations agree ({expected})")


if __name__ == "__main__":
    print("Running version consistency tests...\n")
    test_all_declared_versions_agree()
    print("\nAll tests passed!")
