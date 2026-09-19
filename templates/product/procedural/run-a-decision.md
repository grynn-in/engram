# Run a Product Decision

The entry point. Every other file in this template is reached from here.
Do not start by picking a framework — start by classifying the decision, then
spend the rigour the class deserves.

## Prerequisites

- The decision is actually yours to make. If it is not, the deliverable is a
  recommendation for whoever owns it, not a choice.
- You can name the thing that will be different afterwards. If you cannot, you
  have a discussion, not a decision.

## Steps

1. **Classify reversibility.** Run [Reversibility Test](reversibility-test.md).
   One-way doors get the full treatment. Two-way doors get a bias to action —
   pick, ship, and set the revisit condition.

2. **Write down what you are actually choosing between.** At least two real
   options, plus "do nothing", which is always an option and is often the one
   nobody scored. An option nobody would pick is padding; remove it.

3. **Pick the instrument:**

   | The question is | Use |
   |---|---|
   | Which of these designs / approaches? | [Score Options (HMD)](score-options-hmd.md) |
   | What do we build next, out of many candidates? | [Prioritise with RICE](prioritise-with-rice.md) |
   | We already chose — how do we record it? | [Write an ADR](write-an-adr.md) |

4. **Ground it before you score it.** Read the code and the live data. Then
   mark each claim as *measured* or *judgement*. A table of judgements dressed
   as measurements is worse than no table.

5. **Decide, and name the trade-off you are accepting.** Not the benefit — the
   cost. A decision with no stated cost has not been made yet.

6. **Record it.** Write the outcome to `vision/` using the shape in
   [`_example-decision.md`](../vision/_example-decision.md): owner, date,
   reasoning, the option rejected and why, and the condition that reopens it.

7. **Set the revisit condition.** Something observable — a date, a metric
   crossing a threshold, a dependency shipping. "When it becomes a problem" is
   not a condition.

## Known failure modes

- Scoring options you were never going to pick, to make the winner look earned.
- Choosing the framework first, then the decision that fits it.
- Recording the decision without the rejected alternative, which is the only
  part a future reader actually needs.
- Attributing a decision to someone who did not make it. If provenance is lost,
  write "provenance unknown" — see [decision anti-patterns](../traps/decision-anti-patterns.md).
