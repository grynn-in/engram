# `engram forget` did not forget — archived files were still searched

**Symptom**: after `engram forget "JWT expiry"`, searching for "JWT expiry"
returned the superseded file as the **#1 hit at 0.919**, ranked above the live
knowledge that replaced it. `engram lint` kept reporting it. `engram xref`
wrote links pointing *at* archived files into live ones.

**Cause**: `forget` moves a file to `<layer>/.archive/`, but nothing excluded
`.archive/` from any memory walk. There were 18 walk sites across the commands
and not one skipped it. Six sites had an ad-hoc `".cache" in str(f)` guard —
each written slightly differently — and `.archive` was simply never considered.

**Cost**: unbounded, and invisible. Every `forget` since the command shipped
was a no-op for retrieval while *appearing* to work: it printed "Superseded",
moved the file, and the content kept coming back. Exit codes never showed it.
The damage also propagated into user content via `xref`.

**Avoid**:
- `SKIP_DIRS` / `is_skipped()` in `lib/layers.py` is the single definition;
  every walk goes through it.
- `tests/test_forget.py` asserts the end-to-end guarantee — forget, then search
  must not return the file — and fails without the fix.
- General rule: **a command whose job is removal needs a test that searches for
  the thing afterwards.** "It moved the file" is not the guarantee; "it stopped
  coming back" is.

**Discovered**: 2026-09-19, while sweeping untested commands. Fixed in a418d2a.

Related: [exit-zero defects](commands-that-exit-zero-and-do-nothing.md)
