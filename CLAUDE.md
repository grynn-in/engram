# Project — Claude Code Reference

<!-- engram:protocol:start -->
## Engram — 7-Layer Memory System

You have a 7-layer memory system in `.claude/memory/`:

| Layer | Path | Purpose |
|-------|------|---------|
| 1. Core Identity | `CLAUDE.md` | Permanent rules, always active |
| 2. Lossless | `memory/lossless/` | Raw session transcripts (append-only) |
| 3. Semantic | `memory/semantic/` | Distilled facts, searchable knowledge |
| 4. Procedural | `memory/procedural/` | Workflows, standards, how-tos |
| 5. Traps | `memory/traps/` | Lessons learned the hard way — what bit you, why, how to avoid it |
| 6. Vision | `memory/vision/` | Where this is going — goals, direction, non-goals, principles |
| 7. Active | `memory/active/` | Today's tasks, context, blockers |

**Retrieval priority**: Active → Semantic → Procedural → Traps → Vision → Lossless

**Session workflow**:
- Start: `engram start "topic"` (or `bash .claude/scripts/engram-start "topic"`)
- Every 30 min: `engram end "summary"` (MANDATORY checkpoint)
- Search: `engram search "query"`

**Update rules**:
- After every 3-4 tool calls: update `active/current-tasks.md`
- After solving a problem: distill learnings → `semantic/`
- After documenting a workflow: write to `procedural/`
- After something breaks or surprises you: write the trap → `traps/`
- When direction or a non-goal is decided: record it → `vision/`
- Never delete memory files — supersede or append with dates
<!-- engram:protocol:end -->
