#!/usr/bin/env python3
"""Engram CLI entry point for pip-installed package."""
import os
import sys
import shutil
import subprocess
from pathlib import Path


def get_bin_dir() -> Path:
    """Find the bin/ directory with engram scripts."""
    # When installed via pip, scripts are bundled in the package
    pkg_dir = Path(__file__).parent
    bin_dir = pkg_dir / "bin"
    if bin_dir.is_dir():
        return bin_dir
    # Fallback: check ENGRAM_HOME
    engram_home = Path(os.environ.get("ENGRAM_HOME", Path.home() / ".engram"))
    return engram_home / "bin"


def find_bash() -> str | None:
    """Locate a real POSIX bash to run engram's shell scripts.

    On Windows we must avoid the WindowsApps ``bash.exe`` stub (that launches
    WSL, a separate filesystem). Prefer Git for Windows' bash. Honor an
    ``ENGRAM_BASH`` override for non-standard installs.
    """
    override = os.environ.get("ENGRAM_BASH")
    if override and Path(override).exists():
        return override

    if os.name != "nt":
        return shutil.which("bash")

    candidates = [
        Path(os.environ.get("ProgramFiles", r"C:\Program Files")) / "Git" / "bin" / "bash.exe",
        Path(os.environ.get("LOCALAPPDATA", "")) / "Programs" / "Git" / "bin" / "bash.exe",
        Path(os.environ.get("ProgramFiles(x86)", r"C:\Program Files (x86)")) / "Git" / "bin" / "bash.exe",
    ]
    for c in candidates:
        if c.exists():
            return str(c)
    # Last resort: a bash on PATH that isn't the WindowsApps WSL stub.
    found = shutil.which("bash")
    if found and "WindowsApps" not in found:
        return found
    return None


def main():
    """Main CLI entry point."""
    bin_dir = get_bin_dir()
    engram_script = bin_dir / "engram"

    if not engram_script.exists():
        print("Error: engram scripts not found.")
        print(f"Searched: {bin_dir}")
        print("Run engram setup, or populate ENGRAM_HOME/bin.")
        sys.exit(1)

    bash = find_bash()
    if not bash:
        print("Error: bash not found. Engram requires bash.")
        print("On Windows, install Git for Windows or set ENGRAM_BASH to a bash.exe.")
        sys.exit(1)

    # MSYS bash resolves paths via readlink -f; pass forward slashes so it
    # doesn't choke on Windows backslashes.
    script_arg = engram_script.as_posix()
    args = [bash, script_arg] + sys.argv[1:]

    # Prepend bin_dir to PATH using the platform separator (MSYS converts a
    # Windows-style PATH to POSIX on startup). The hardcoded ":" was a bug.
    new_path = f"{bin_dir}{os.pathsep}{os.environ.get('PATH', '')}"
    try:
        result = subprocess.run(args, env={**os.environ, "PATH": new_path})
        sys.exit(result.returncode)
    except FileNotFoundError:
        print("Error: bash not found. Engram requires bash.")
        sys.exit(1)


if __name__ == "__main__":
    main()
