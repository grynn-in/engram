# Adding a layer is not shipping it — existing projects saw nothing

**Symptom**: after adding `traps/` and `vision/`, re-running `engram init` on an
existing project created both directories and printed success. The project's
`CLAUDE.md` still said "5-Layer Memory System" and never mentioned either
layer. The directories stayed empty forever.

**Cause**: `engram init` checked `grep -q "## Engram" CLAUDE.md` and, on a hit,
printed "already has Engram protocol — skipped". The check answered "is there a
protocol block?" when the question was "is the protocol block *current*?".
`schema.md` had the identical hole — copied only when absent.

**Cost**: would have been total. The feature reaches only projects created after
the release; every existing user gets empty directories and no instruction to
use them. Caught before release, but only because the upgrade path was tested
explicitly rather than assumed.

**Avoid**:
- Fence generated blocks (`<!-- engram:protocol:start -->`) so they can be
  rewritten in place without touching what a project wrote around them.
- Presence checks are not version checks. Compare content, not existence.
- **Ship every schema/layer/protocol change with a migration test that starts
  from the previous version's output and asserts the result is byte-identical to
  a fresh install.** `tests/test_migration.py` does exactly this.
- For files a user may edit (`schema.md`), ship digests of every version you
  have released; refresh only on a match, and say so when you decline.

**Discovered**: 2026-09-19, asking "what's next" rather than assuming done.
Fixed in a16eb41.

Related: [exit-zero defects](commands-that-exit-zero-and-do-nothing.md)
