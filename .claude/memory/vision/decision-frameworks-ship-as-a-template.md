# Decision frameworks are opt-in, not baked into every project

**Status**: Accepted

**Intent**
Product decision frameworks ship as `templates/product/`, reached via
`engram init --template product`. Engram stays unopinionated by default.

**Context**
Four frameworks were wanted: the reversibility test, HMD option scoring, ADRs,
and RICE/ICE. They route into each other from `procedural/run-a-decision.md`
rather than sitting in a list — classify the decision first, then spend the
rigour the class deserves.

**Alternatives rejected**
- *Bake them into `templates/default/schema.md`*, so every new project gets them.
  Rejected as opinionated: it imposes one decision style on every project, and
  "not opinionated" is a criterion engram is scored by.
- *A separate `decisions/` layer.* Rejected: the registry had just made adding a
  layer cheap, which is not the same as it being right. `vision/` already holds
  decisions with owner, date and alternatives-rejected.

**Consequences**
- Easier: frameworks are one flag away, and `traps/`+`vision/` get a real first
  customer.
- Harder: template CLAUDE.md guidance now lives in `claude.md.extra` with the
  snippet generated from it — one more generated artifact to keep honest. A test
  enforces it.

**Owner**: Deepak Pai, 2026-09-19

**Revisit when**: more than ~3 templates want the same guidance block. That
would argue for composable template fragments instead of per-template extras.
