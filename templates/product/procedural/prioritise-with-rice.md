# Prioritise with RICE (and when ICE is enough)

For ranking many candidates against each other — a backlog, a quarter, a list
of bets. Not for choosing between designs; that is [Score Options](score-options-hmd.md).

## Prerequisites

- A list of candidates that are roughly comparable in kind.
- A number you can actually get for Reach. If you cannot measure reach, use ICE
  and say so, rather than inventing a number that then gets multiplied.

## Steps

1. Score each candidate:

   | Factor | Meaning | Unit |
   |---|---|---|
   | **R**each | How many are affected per period | Count per quarter — measured, not guessed |
   | **I**mpact | How much it moves the thing you care about, per affected user | 3 massive / 2 high / 1 medium / 0.5 low / 0.25 minimal |
   | **C**onfidence | How much you believe the above | 100% measured / 80% some data / 50% informed guess |
   | **E**ffort | Total person-months, all functions, including review and rollout | Person-months |

2. `RICE = (Reach × Impact × Confidence) / Effort`.

3. Rank, then **look at the ranking and check whether you believe it.** If the
   top item feels wrong, the model is missing a factor — usually a dependency,
   a deadline, or a strategic commitment that is not a score. Add it as a
   constraint outside the formula; do not bend the numbers until they agree.

4. Use **ICE** (Impact × Confidence / Effort) when reach is unknowable or
   identical across candidates. It is the same tool with one fewer invented
   number, which usually makes it the more honest one.

5. Record the ranking with its date in `vision/`. Scores are a snapshot of what
   you knew; they expire, and an undated ranking gets cited forever.

## Known failure modes

- Tuning Confidence until the answer matches the intuition. If that is what is
  happening, the intuition is the real input — write it down and defend it
  directly.
- Effort estimated by the engineer who wants to build it.
- Treating the output as a decision rather than a starting order. RICE ranks;
  people decide.
- Comparing a research spike against a shipped feature. Different kinds, not
  comparable — split the list.
