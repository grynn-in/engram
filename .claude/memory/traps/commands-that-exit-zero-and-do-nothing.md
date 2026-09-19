# The dangerous defect class here is exit-zero-and-wrong, not crashes

**Symptom**: I predicted that 29 untested commands would be full of crashes.
Exercising all 38 commands plus their subcommands and flags found exactly
**one** crash. The code was more robust than expected — and that was the
misleading part.

**Cause**: four of the five defects found that day exited 0 and printed a
plausible success message while doing the wrong thing:

| Command | Exit | What it printed | What it did |
|---|---|---|---|
| `forget` | 0 | "Superseded: …" | content still #1 in search |
| `index` | 0 | normal output | ignored the entire config file |
| `compound` | 0 | "No results found" | search had 8 results |
| `export-obsidian` | 0 | "Exported N files" | discarded every link label |

**Cost**: these had shipped for months. A smoke test that asserts `rc == 0`
would have passed on all four, forever.

**Avoid**: for each command, write the test that asserts the *effect*, not the
exit code — search after forget, read the config back after index, count
results after compound. If the assertion is "it ran", it is not a test.

**Discovered**: 2026-09-19.

Related: [the forget trap](forget-did-not-forget-archived-files-still-searched.md),
[the importlib trap](compound-crashed-on-importlib-machinery.md)
