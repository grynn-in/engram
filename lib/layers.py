#!/usr/bin/env python3
"""
Engram layer registry — the single source of truth for memory layers.

Every command that needs to know which layers exist, what order they come in,
how they score in search, or whether they travel between projects reads it from
here. Adding a layer means adding one entry to LAYERS below; no other file in
the codebase should hardcode a layer name.

Consumed by:
  Python commands   sys.path.insert(0, SCRIPT_DIR.parent / "lib")
                    from layers import ALL_LAYERS, search_bonus, ...
  Bash commands     source "$LIB_DIR/layers.sh"
                    for layer in $(engram_layers all); do ...

Named sets (see layer_set):
  all           every layer directory, in retrieval-priority order
  curated       hand-written knowledge — lint / xref / contradict scan these
  searchable    curated + working context — what forget and recall walk
  transferable  layers that travel via sync, export and templates
  shared        layers multiple agents read and write under lock
  session       session state, not durable knowledge
  append_only   layers that are written once and never edited
"""

import json
import sys
from dataclasses import dataclass, asdict
from pathlib import Path


@dataclass(frozen=True)
class Layer:
    """One memory layer. Order in LAYERS is retrieval priority."""

    name: str            # directory name under .claude/memory/
    title: str           # display name, e.g. "Traps"
    purpose: str         # one line, used in generated docs and CLAUDE.md
    search_bonus: float  # multiplier delta applied by engram-search
    curated: bool        # hand-written knowledge (lint/xref/contradict scan it)
    transferable: bool   # travels via sync / export / templates
    append_only: bool    # written once, never edited (audit trail)
    writes: str          # when Claude should write here — shown in protocol
    doc_rank: int        # position in the numbered CLAUDE.md table (see DOC ORDER)


# ---------------------------------------------------------------------------
# The registry. Add a layer here and every command picks it up.
# ---------------------------------------------------------------------------
LAYERS = (
    Layer(
        name="active",
        title="Active",
        purpose="Today's tasks, context, blockers",
        search_bonus=0.00,
        curated=False,
        transferable=False,
        append_only=False,
        writes="After every 3-4 tool calls: update `active/current-tasks.md`",
        doc_rank=7,
    ),
    Layer(
        name="semantic",
        title="Semantic",
        purpose="Distilled facts, searchable knowledge",
        search_bonus=0.10,
        curated=True,
        transferable=True,
        append_only=False,
        writes="After solving a problem: distill learnings → `semantic/`",
        doc_rank=3,
    ),
    Layer(
        name="procedural",
        title="Procedural",
        purpose="Workflows, standards, how-tos",
        search_bonus=0.05,
        curated=True,
        transferable=True,
        append_only=False,
        writes="After documenting a workflow: write to `procedural/`",
        doc_rank=4,
    ),
    Layer(
        name="traps",
        title="Traps",
        purpose="Lessons learned the hard way — what bit you, why, how to avoid it",
        search_bonus=0.15,
        curated=True,
        transferable=True,
        append_only=False,
        writes="After something breaks or surprises you: write the trap → `traps/`",
        doc_rank=5,
    ),
    Layer(
        name="vision",
        title="Vision",
        purpose="Where this is going — goals, direction, non-goals, principles",
        search_bonus=0.05,
        curated=True,
        transferable=True,
        append_only=False,
        writes="When direction or a non-goal is decided: record it → `vision/`",
        doc_rank=6,
    ),
    Layer(
        name="lossless",
        title="Lossless",
        purpose="Raw session transcripts (append-only)",
        search_bonus=-0.10,
        curated=False,
        transferable=False,
        append_only=True,
        writes="Written automatically by `engram end` — never edit by hand",
        doc_rank=2,
    ),
)

BY_NAME = {layer.name: layer for layer in LAYERS}

# LAYERS is in retrieval-priority order — that is what iteration and display use.
# The numbered table in CLAUDE.md runs raw -> refined -> working instead, which is
# the numbering existing projects already have; doc_rank preserves it.
DOC_ORDER = sorted(LAYERS, key=lambda l: l.doc_rank)

# Fail loudly at import if the ranks stop being 2..N+1 with no gaps or repeats:
# a silently wrong table would renumber every project's CLAUDE.md.
_ranks = [l.doc_rank for l in DOC_ORDER]
if _ranks != list(range(2, len(LAYERS) + 2)):
    raise ValueError(
        "layer doc_rank must be 2..%d exactly once each (CLAUDE.md is layer 1); got %s"
        % (len(LAYERS) + 1, _ranks)
    )

# Ordered name lists. Prefer these over re-deriving from LAYERS.
ALL_LAYERS = [l.name for l in LAYERS]
CURATED_LAYERS = [l.name for l in LAYERS if l.curated]
TRANSFERABLE_LAYERS = [l.name for l in LAYERS if l.transferable]
SESSION_LAYERS = [l.name for l in LAYERS if not l.curated]
APPEND_ONLY_LAYERS = [l.name for l in LAYERS if l.append_only]
# Everything a person or Claude edits by hand — i.e. all but the append-only
# history. What search, forget, recall and the default export walk.
SEARCHABLE_LAYERS = [l.name for l in LAYERS if not l.append_only]
# Layers several agents may touch at once; writes need a lock.
SHARED_LAYERS = list(CURATED_LAYERS)

# Directories inside a layer that are not live knowledge. Every walk over memory
# must skip them:
#   .cache/    machine-local embedding cache, regenerated on demand
#   .archive/  files superseded by `engram forget`. The whole point of forget is
#              that the content stops coming back — while these were still
#              walked, a forgotten file came back as the top search hit,
#              outranking the live knowledge that replaced it.
SKIP_DIRS = frozenset({".cache", ".archive"})


def is_skipped(path) -> bool:
    """True if a path sits inside a non-live directory (see SKIP_DIRS)."""
    return any(part in SKIP_DIRS for part in Path(str(path)).parts)


def iter_layer_files(memory_root, layers=None, pattern="*.md"):
    """Yield (layer, path) for live knowledge files, skipping SKIP_DIRS."""
    root = Path(memory_root)
    for layer in (ALL_LAYERS if layers is None else layers):
        layer_dir = root / layer
        if not layer_dir.is_dir():
            continue
        for f in sorted(layer_dir.rglob(pattern)):
            if f.is_file() and not is_skipped(f):
                yield layer, f


SETS = {
    "all": ALL_LAYERS,
    "curated": CURATED_LAYERS,
    "searchable": SEARCHABLE_LAYERS,
    "transferable": TRANSFERABLE_LAYERS,
    "shared": SHARED_LAYERS,
    "session": SESSION_LAYERS,
    "append_only": APPEND_ONLY_LAYERS,
}

# CLAUDE.md is layer 1 (core identity); the directories are the rest.
LAYER_COUNT = len(LAYERS) + 1


def layer_set(name):
    """Return the ordered layer names in a named set. Raises on unknown names."""
    try:
        return list(SETS[name])
    except KeyError:
        raise KeyError(
            "unknown layer set %r (have: %s)" % (name, ", ".join(sorted(SETS)))
        )


def layer_of(path):
    """Return the layer a path belongs to, or None if it is outside every layer."""
    parts = str(path).replace("\\", "/").split("/")
    for part in reversed(parts):
        if part in BY_NAME:
            return part
    return None


def search_bonus(path):
    """Return the search-score delta for a path's layer (0.0 if outside a layer)."""
    name = layer_of(path)
    return BY_NAME[name].search_bonus if name else 0.0


def bonus_summary():
    """Human-readable layer bonuses, for docstrings and --help output."""
    return ", ".join(
        "%s (%+d%%)" % (l.name, round(l.search_bonus * 100)) for l in LAYERS
    )


def protocol_block():
    """The '## Engram' section injected into a project's CLAUDE.md."""
    rows = ["| 1. Core Identity | `CLAUDE.md` | Permanent rules, always active |"]
    for l in DOC_ORDER:
        rows.append("| %d. %s | `memory/%s/` | %s |" % (l.doc_rank, l.title, l.name, l.purpose))

    priority = " → ".join(l.title for l in LAYERS)
    writes = "\n".join("- %s" % l.writes for l in LAYERS if l.curated or l.name == "active")

    return """## Engram — {n}-Layer Memory System

You have a {n}-layer memory system in `.claude/memory/`:

| Layer | Path | Purpose |
|-------|------|---------|
{rows}

**Retrieval priority**: {priority}

**Session workflow**:
- Start: `engram start "topic"` (or `bash .claude/scripts/engram-start "topic"`)
- Every 30 min: `engram end "summary"` (MANDATORY checkpoint)
- Search: `engram search "query"`

**Update rules**:
{writes}
- Never delete memory files — supersede or append with dates
""".format(n=LAYER_COUNT, rows="\n".join(rows), priority=priority, writes=writes)


def _main(argv):
    """CLI used by layers.sh and by anything that wants the registry as data."""
    arg = argv[1] if len(argv) > 1 else "all"

    if arg == "--json":
        json.dump([asdict(l) for l in LAYERS], sys.stdout, indent=2)
        sys.stdout.write("\n")
        return 0
    if arg == "--protocol":
        sys.stdout.write(protocol_block())
        return 0
    if arg == "--count":
        print(LAYER_COUNT)
        return 0
    if arg in ("--sets", "--help", "-h"):
        print("usage: layers.py [%s|--json|--protocol|--count]" % "|".join(sorted(SETS)))
        return 0

    try:
        print("\n".join(layer_set(arg)))
    except KeyError as exc:
        print(exc.args[0], file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(_main(sys.argv))
