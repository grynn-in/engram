# Score Options (HMD — "Help Me Decide")

For one-way doors, and for any choice where the options differ in kind rather
than in degree. The output is a table of options, not a recommendation dressed
as the only path — and not code. Do not start building until the owner picks.

## Prerequisites

- [Reversibility test](reversibility-test.md) says this is worth the effort.
- Two or more real options, each one someone would actually defend.
- You have read the code and looked at the live data. Scoring from memory
  produces a table of guesses with the authority of a table.

## Steps

1. **One table.** Criteria as rows, options as columns. Cells terse: a verdict
   plus a few words. Keep every row, marking `n/a` where a criterion does not
   apply — the empty rows are information. They show what the choice does not
   touch, which is how a reader knows you considered it.

2. **Use these criteria.** Adapt the set to the domain, but drop a row only
   deliberately, never because it was inconvenient.

   | Criterion | What it asks |
   |---|---|
   | Product, not one-off | Does it work for a customer whose data, chart or policy differs? |
   | Technical debt | What it leaves behind: dead fields, silent fallbacks, tests that cannot fail, two sources of truth, a rule maintained by hand |
   | Configurable | Can a customer express their policy without code? |
   | Not opinionated | No silent default deciding policy for them; an unavoidable default is declared and visible |
   | Compliant | Defensible under the standard, and auditable |
   | No silent fallback | Every fallback is visible: named in a test, a warning, or a build failure |
   | Traceable | The decision carries an owner, a date, a reason and the alternative rejected, and the code cites it |
   | Effective-dated | Anything that drives a number carries a validity window from the start |
   | Bounded residual | Where a plug exists, it is small enough to explain and decomposable when it is not |
   | Upgrade path | The change ships with what an existing deployment does about it |

3. **Then, in a few lines:** which you would take and why, the trade-off it
   accepts, any prerequisite that must land first, and what would have to be
   true to pick another. That last clause is the one that makes the table
   falsifiable.

4. **Mark your evidence.** Say which claims are measured and which are
   judgement. Mixing them silently is the most common way a table lies.

5. **After the owner decides**, record it with provenance: a `vision/` entry
   naming who decided, the date, the reasoning and the option rejected. Never
   attribute a decision to someone who did not make it; if a prior decision
   cannot be traced to a person, say so rather than building on it.

## Known failure modes

- Filling the table to justify the option you had already chosen. If every row
  favours one column, you have written an argument, not an analysis.
- Dropping the rows that make your preferred option look bad.
- Producing a recommendation when the owner asked for options.
- Scoring "technical debt" as a feeling instead of naming the specific artifact
  left behind.
