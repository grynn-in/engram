# Reversibility Test (One-Way vs Two-Way Doors)

Classify before you deliberate. Most decisions are cheaper to make than to
discuss, and applying heavyweight process to them is itself a cost.

## Prerequisites

- A specific decision, not a theme.

## Steps

1. Ask: **if this turns out wrong, what does undoing it cost?** Answer in time
   and blast radius, not in feelings.

2. Place it:

   | | One-way door | Two-way door |
   |---|---|---|
   | Undo cost | Weeks+, or impossible | Hours to days |
   | Blast radius | Data, customers, public API, contracts | Internal, reversible in a branch |
   | Examples | Storage format, pricing model, auth scheme, anything a customer builds on | Library choice, internal layout, feature flag default |
   | Deserves | Full scoring, written record, second opinion | Pick, ship, revisit |

3. **Two-way door**: choose the option you can reverse fastest, ship it, and
   write one line in `vision/` with the revisit condition. Stop. Do not open a
   scoring table.

4. **One-way door**: continue to [Score Options (HMD)](score-options-hmd.md),
   and get someone who disagrees with you to read it.

5. **When unsure, ask what would make it two-way.** A migration path, an
   abstraction, a flag, a contract with an end date. Buying reversibility is
   usually cheaper than buying certainty.

## Known failure modes

- Treating everything as one-way, and shipping nothing.
- Treating a schema or a public interface as two-way because the code is easy
  to change. The code is not the thing that is hard to reverse — the data and
  the people depending on it are.
- Forgetting that *not deciding* is itself a one-way door once the window closes.
