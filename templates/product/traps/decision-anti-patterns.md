# Decision anti-patterns that cost real time

**Symptom**: a decision gets made, then quietly re-made three months later, or
a framework produces a ranking nobody acts on.

**Cause**: each of the patterns below. They are listed with what they look like
from the inside, because that is the only vantage point you get at the time.

## The table built backwards

*Looks like*: every row favours the same column.
*Really is*: the conclusion was reached first, and the criteria were chosen to
support it.
*Avoid*: write the criteria before you look at the options. If a criterion only
occurs to you after seeing which option it helps, say so in the file.

## Provenance laundering

*Looks like*: "we decided to use X" in a doc with no name and no date.
*Really is*: nobody decided; someone did it and it stuck. The next person
inherits it as a constraint and will not challenge it, because it reads like a
decision.
*Cost*: unbounded — this one compounds.
*Avoid*: every entry in `vision/` names a person and a date, or explicitly says
"provenance unknown — this is how it is, not how it was chosen."

## The undated score

*Looks like*: a RICE ranking cited in a planning meeting nine months on.
*Really is*: a snapshot of what was known at a moment, being used as a standing
fact.
*Avoid*: date every ranking, and put its expiry in the file.

## Rigour applied to a two-way door

*Looks like*: three weeks of analysis on a choice that could have been reversed
in an afternoon.
*Really is*: the reversibility test was skipped.
*Cost*: the analysis time, plus everything not decided while it ran.
*Avoid*: classify first. Always.

## Consensus mistaken for a decision

*Looks like*: everyone agreed in the meeting; nothing changed afterwards.
*Really is*: no owner, so no one was obliged to act.
*Avoid*: a decision has exactly one owner. Write the name down in the room.

## The missing "do nothing" column

*Looks like*: three options, all of which involve building something.
*Really is*: the status quo was never scored, so its cost is unknown and its
benefits are invisible.
*Avoid*: "do nothing" is always a column. Sometimes it wins.

**Discovered**: ongoing — add yours here rather than starting a new file.
