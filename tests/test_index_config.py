#!/usr/bin/env python3
"""Tests for engram-index config parsing.

Regression: load_config() guessed a key's TOML section with
content.find(key), which always found the FIRST occurrence in the file. With a
config that sets url under both [embedding] and [vector_db], neither was
applied — engram index silently indexed against the hardcoded localhost
defaults no matter what the user configured.
"""

import importlib.machinery
import importlib.util
import os
import tempfile
from pathlib import Path

ROOT = Path(__file__).parent.parent

CONFIG = """\
# Engram configuration
[embedding]
provider = "ollama"
model = "custom-embed-model"
url = "http://embed-host:9999"

[vector_db]
enabled = true
provider = "qdrant"
url = "http://qdrant-host:7777"
"""


def load_index_module(config_path: str):
    os.environ["ENGRAM_CONFIG"] = config_path
    loader = importlib.machinery.SourceFileLoader("engram_index", str(ROOT / "bin" / "engram-index"))
    spec = importlib.util.spec_from_loader("engram_index", loader)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_urls_are_read_from_their_own_sections():
    with tempfile.TemporaryDirectory() as tmp:
        cfg = Path(tmp) / "config.toml"
        cfg.write_text(CONFIG)
        m = load_index_module(str(cfg))

        assert "qdrant-host:7777" in m.QDRANT_URL, \
            f"[vector_db] url ignored; got {m.QDRANT_URL}"
        assert "embed-host:9999" in m.OLLAMA_URL, \
            f"[embedding] url ignored; got {m.OLLAMA_URL}"
        assert m.OLLAMA_URL.endswith("/api/embeddings"), \
            f"ollama endpoint path lost; got {m.OLLAMA_URL}"
        assert m.EMBEDDING_MODEL == "custom-embed-model", \
            f"[embedding] model ignored; got {m.EMBEDDING_MODEL}"
        print("  PASS: each url is read from its own TOML section")


def test_missing_config_uses_defaults():
    with tempfile.TemporaryDirectory() as tmp:
        m = load_index_module(str(Path(tmp) / "absent.toml"))
        assert m.QDRANT_URL and m.OLLAMA_URL, "defaults should survive a missing config"
        print("  PASS: a missing config falls back to defaults")


def test_comments_and_inline_comments_are_stripped():
    with tempfile.TemporaryDirectory() as tmp:
        cfg = Path(tmp) / "config.toml"
        cfg.write_text('[embedding]\nmodel = "m1"  # trailing comment\n')
        m = load_index_module(str(cfg))
        assert m.EMBEDDING_MODEL == "m1", f"inline comment leaked: {m.EMBEDDING_MODEL!r}"
        print("  PASS: inline comments are stripped")


if __name__ == "__main__":
    print("Running engram-index config tests...\n")
    try:
        test_urls_are_read_from_their_own_sections()
        test_missing_config_uses_defaults()
        test_comments_and_inline_comments_are_stripped()
    finally:
        os.environ.pop("ENGRAM_CONFIG", None)
    print("\nAll tests passed!")
