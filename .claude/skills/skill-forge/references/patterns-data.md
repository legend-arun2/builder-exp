# Pattern: data and analysis skills

For skills that answer recurring questions from data: metric lookups, standard reports,
investigations that follow a known path.

## What makes these effective

- **Definitions over technique.** The model can already write SQL. It cannot know that
  "active user" means a login in the last 28 days excluding staff. Put the definitions,
  the right tables and the standing filters first.
- **Name the traps.** Tables that look right but are not, columns whose meaning changed
  on a date, time-zone and currency handling, duplicates. Give the reason for each so
  related traps are recognised too.
- **A sanity check per answer.** A known total to reconcile against, an expected range,
  a row-count check. Wrong numbers that look plausible are the main risk.
- **Schema in a reference file.** Table and column listings are long and needed only
  when writing a query: `references/schema.md`, read on demand.
- **A fixed answer shape.** The number, its exact definition, the period, caveats, and
  the query used, so results can be compared between runs and checked by a person.

## Skeleton

```markdown
# <Name>

<Goal: which questions this answers and for whom.>

## Sources
- <Dialect / connection / tool to run queries with.>
- Read `references/schema.md` before writing a query.

## Definitions
- **<Metric>** — <exact definition, including filters and grain>.

## Standing rules
- <Rule> — <reason>.

## Steps
1. Restate the question with the period and definition you will use; ask only if
   it is ambiguous in a way that changes the number.
2. Write the query. <Conventions: CTEs, date handling.>
3. Sanity-check: <specific check>.
4. Report.

## Output
<Answer first, then definition, period, caveats, query.>

## If something goes wrong
- Empty result → <check>. Numbers off against <reference> by more than <x> → <action>.
```

## Example (abridged)

```markdown
---
name: revenue-metrics
description: Answers MRR, churn and net revenue retention questions from the billing warehouse using the finance team's definitions. Use when the user asks about MRR, ARR, churn, retention, expansion or revenue by plan or cohort. Not for product usage or event analytics.
---

# Revenue metrics

## Definitions
- **MRR** — sum of `amount_monthly_usd` over subscriptions with `status = 'active'` on
  the last day of the month.
- **Churned MRR** — MRR of subscriptions active at the end of last month and not at the
  end of this month. Downgrades are contraction, not churn.

## Standing rules
- Use `billing.subscriptions_daily`, not `billing.subscriptions` — the latter holds only
  current state, so any historical question comes out wrong.
- Exclude `is_internal = true`; staff accounts add about 2% to MRR.
- Months are calendar months in UTC, which is what finance reports use.

## Sanity check
Month-end MRR should be within 0.5% of `finance.mrr_reported`. If it is not, say so and
show both numbers instead of presenting yours as correct.

## Output
One-line answer, then: definition used, period, caveats, and the query in a code block.
```

## Script candidates

Running a parameterised standard query, reconciling against a reference total, turning
a result set into the standard chart or table.
