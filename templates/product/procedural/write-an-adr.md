# Write an ADR (Architecture Decision Record)

How to record a decision once it is made, so that a reader a year later can
tell whether it still holds. One file per decision, in `vision/`.

## Prerequisites

- The decision is made. An ADR is a record, not a deliberation — if you are
  still choosing, you want [Score Options](score-options-hmd.md).

## Steps

1. Create `vision/{decision-slug}.md`. Name it after the decision, not the
   technology: `no-cloud-by-default.md`, not `about-sync.md`.

2. Fill these sections. Each one earns its place:

   - **Status** — Proposed / Accepted / Superseded by `[[other-decision]]`.
     Never delete a superseded ADR; the trail is the point.
   - **Context** — what was true that forced a choice. Constraints, deadlines,
     what you measured. Written so a reader who was not there understands the
     pressure.
   - **Decision** — one sentence, active voice: "We will …".
   - **Alternatives rejected** — each with the reason it lost. This is the
     section future readers actually come for, and the one most often skipped.
   - **Consequences** — what becomes easier, and what becomes harder. Both.
     An ADR with only upsides is marketing.
   - **Owner and date** — who decided, when.
   - **Revisit when** — the observable condition that reopens this.

3. Link it from the code that implements it. A decision the code does not cite
   is a decision the code will drift away from.

4. When it is superseded, edit only the Status line and add the link. Leave
   everything else exactly as written, including the parts that turned out
   wrong — they are the evidence for why the next decision was different.

## Known failure modes

- Writing the ADR after the code, from the code. It then records what was built,
  not what was decided, and the alternatives section comes out empty.
- "Consequences: none." There are always consequences; not knowing them is a
  finding worth writing down.
- One ADR covering three decisions. Split it — each needs its own status.
