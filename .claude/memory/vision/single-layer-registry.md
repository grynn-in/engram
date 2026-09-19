# Layers are defined once, in lib/layers.py

**Status**: Accepted

**Intent**
Adding a memory layer costs one entry in `LAYERS`. Everything else — the
CLAUDE.md protocol table, search scoring, sync/export/template sets, the web UI
tabs, lint and xref coverage — follows from it.

**Context**
Two new layers were needed. Layer names were hardcoded in ~102 places across 30
files, and the lists had already drifted: `engram-diff` iterated 3 layers in one
function and 4 in another. Measured by grep before starting, not estimated.

**Alternatives rejected**
- *Append the two names to each of the ~102 sites.* Ships faster, leaves the
  drift, and charges the same 102 edits next time. Rejected: the cost is paid
  by whoever comes next, every time.
- *Registry for the new layers only, rest left hardcoded.* Rejected: two sources
  of truth is precisely the failure being removed, and the hardcoded half is the
  half that silently diverges.

**Consequences**
- Easier: a layer is one entry; the 8th costs nothing.
- Harder: a registry change touches every command at once, so the drift tests
  are load-bearing. `tests/test_layers.py` fails the build if any `bin/` command
  re-lists the layers, or if a generated file stops matching its generator. If
  those tests are ever skipped, the guarantee is gone.

**Owner**: Deepak Pai, 2026-09-19

**Revisit when**: a layer needs per-project configuration. The registry is
compile-time today; that is the assumption that would break.

See also: [traps and vision are transferable](traps-and-vision-are-transferable.md)
