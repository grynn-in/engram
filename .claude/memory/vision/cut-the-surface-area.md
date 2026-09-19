# Proposal: cut the supported command surface from 38 to ~12

**Status**: Proposed — NOT decided. Do not treat this as agreed.

**Intent**
Reduce `engram --help` to the commands that are load-bearing and tested, and
move the rest behind `engram lab <cmd>` or delete them.

**Context (measured 2026-09-19)**
- 38 commands, 10,158 lines in `bin/` + `lib/`.
- 13 test files, ~1,275 lines. 29 of 38 commands had no test.
- A one-day sweep of the untested surface found 5 defects. Only 1 was a crash;
  4 exited 0 while doing the wrong thing, two of them silently
  (`forget`, `index`). See [exit-zero defects](../traps/commands-that-exit-zero-and-do-nothing.md).

**The argument**
Not that the untested commands crash — they mostly do not. It is that they fail
*quietly*, and verifying 38 commands to the depth that catches quiet failure is
not affordable. A smaller supported set that is actually tested is a more honest
product than a large one with unknown reliability.

Candidate supported set: `init, start, end, search, recall, status, sync,
export, import, lint, index, template`.

**Alternatives not yet weighed**
- Keep all 38 and require a test per command (~1 week, higher ceiling).
- Ship as-is and let usage decide what matters.

**Owner**: unassigned. This is a recommendation from Claude, not a decision by
Deepak Pai — do not cite it as one. Provenance of this file: written
2026-09-19 during the layer-registry work.

**Revisit when**: before the 0.8.0 release announcement, since it changes what
is advertised.
