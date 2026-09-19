# traps/ and vision/ travel between projects

**Status**: Accepted

**Intent**
`traps/` and `vision/` are transferable: they sync, export, and seed templates
alongside `semantic/` and `procedural/`.

**Context**
A trap is the most expensive knowledge to re-learn, which is why it carries the
highest search bonus (+15%). A lesson about a stack applies to the next project
on that stack.

**Alternatives rejected**
- *traps transferable, vision not.* This was the recommendation — one project's
  direction is meaningless in another. Rejected by the owner so that a house
  "vision" (team principles, standing non-goals) can seed every new project.
- *Neither transferable*, on privacy grounds, since traps may quote real
  incidents. Rejected: hard-won lessons would die with the project. Mitigation is
  `engram pii scan` before sharing a template, not making the layer local.

**Consequences**
- Easier: `engram template create` captures decisions and traps, not just facts.
- Harder: `traps/` may contain incident detail, so anything leaving the machine
  needs a PII pass first. This is a real obligation, not a note.

**Owner**: Deepak Pai, 2026-09-19

**Revisit when**: a template is published publicly and a trap turns out to carry
customer-identifying detail. That would argue for a per-file `shareable` flag
rather than a per-layer one.
