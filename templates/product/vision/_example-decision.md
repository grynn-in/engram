# Example: the shape a decision record takes

**Status**: Example — delete this file once you have written a real one.

This file exists to show the shape. Every decision in `vision/` should be
readable a year later by someone who was not in the room.

---

# Ship the memory layers as one registry, not two lists

**Status**: Accepted

**Context**
Two new memory layers were needed. The layer names were hardcoded in roughly a
hundred places across two dozen commands, and the lists had already drifted —
one command iterated three layers in one function and four in another. Measured
by grep before starting; not an estimate.

**Decision**
We will define the layers once, in a registry, and have every command read the
set it needs from it.

**Alternatives rejected**
- *Append the two names to each existing list.* Rejected: ships faster, but
  leaves the drift in place and prices the next layer at the same hundred
  edits. The cost is paid every time, by whoever comes next.
- *Registry for the new layers only, leaving the rest hardcoded.* Rejected:
  two sources of truth is the failure we were trying to remove, and the half
  that stays hardcoded is the half that silently diverges.

**Consequences**
- Easier: adding a layer is one entry; the CLAUDE.md table, the web UI tabs and
  the sync sets all follow.
- Harder: a change to the registry now touches every command at once, so the
  drift tests are load-bearing. If they are ever skipped, the guarantee is gone.

**Owner**: <NAME>, <YYYY-MM-DD>

**Revisit when**: a layer needs per-project configuration — the registry is
compile-time today, and that is the assumption that would break.
