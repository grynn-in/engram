# Guessing a TOML section with `content.find(key)` drops every value

**Symptom**: `engram index` used hardcoded localhost URLs no matter what
`~/.config/engram/config.toml` said. Both `[embedding].url` and
`[vector_db].url` were silently discarded. Pointing engram at a remote Qdrant
indexed against localhost with no warning.

**Cause**: the hand-rolled parser worked out which section a key belonged to with

```python
if key == "url" and "qdrant" in content[:content.find(key)].rsplit("[", 1)[-1]:
```

`content.find(key)` searches the **whole file from the start**, so it always
returned the position of the *first* `url` — under `[embedding]`. The check
therefore evaluated identically for every `url` line in the file, and matched
neither. Separately, `OLLAMA_URL` was declared `global` and never assigned at
all, so that branch could not have worked regardless.

**Cost**: silent. Config appeared to be supported; it was inert. Anyone running
a non-default host got wrong behaviour with no signal.

**Avoid**:
- Track the current section as you iterate lines. Never infer position-dependent
  context with a whole-file search.
- Prefer `tomllib` (3.11+) over hand-rolling, unless the 3.9 floor is real.
- `except Exception: pass` around config loading hid it; it now warns to stderr.
- Test config parsing against a file that sets **the same key in two sections** —
  that is the case that exposes this whole class of bug.

**Discovered**: 2026-09-19, via a pyflakes "unused global" hint that turned out
to be load-bearing. Fixed in a418d2a, covered by `tests/test_index_config.py`.
