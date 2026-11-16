# Writing a skill that works

## How a skill is loaded

1. **Always in context:** only the `name` and `description` of every installed skill.
2. **When triggered:** the body of `SKILL.md`.
3. **On demand:** any other file in the folder, when the body says to read or run it.

So the description must win the decision to load, the body must be worth its space on
every run, and everything else should wait in separate files.

## Frontmatter

```yaml
---
name: release-notes
description: <what it does>. Use when <triggers>. Not for <near-misses>.
---
```

- `name` — lowercase letters, digits and hyphens; at most 64 characters; same as the
  folder name.
- `description` — at most 1024 characters, on one line or as a folded block.
- Optional fields, only when needed:
  - `argument-hint` — shown when the user types `/<name>`, e.g. `"[version]"`.
  - `allowed-tools` — tools the skill may use without asking.
  - `disable-model-invocation: true` — the skill runs only when the user types
    `/<name>`. Use for anything with side effects the user must start deliberately
    (deploys, sending messages).

## The description

Formula: **what it does** + **when to use it** + **what it is not for**.

Write it in the third person and include the words the user really types. The model
matches requests against this text, so vocabulary matters more than elegance. Lean
slightly towards triggering: an unused skill is the more common failure.

| Weak | Strong |
|---|---|
| Helps with releases. | Drafts release notes from merged pull requests since the last tag and updates CHANGELOG.md. Use when the user asks for release notes, a changelog entry, "what shipped", or is preparing a version bump. Not for writing commit messages. |
| Data helper for our warehouse. | Answers revenue and retention questions against the analytics warehouse using the team's metric definitions. Use when the user asks about MRR, churn, retention, cohort or revenue numbers, or wants a query on the `billing` tables. Not for product-event analysis. |

Checks: Would it match each trigger phrase from the interview? Would it wrongly match
the near-miss? Does it avoid "I" and "you"?

## The body

**Lead with the goal.** One or two sentences on what a good outcome is. With the goal
in view, the model can make sensible choices where the steps run out.

**Write steps as instructions, in order.** "Run the tests", not "the tests should be
run". Number steps when order matters; use bullets when it does not.

**Give the reason for non-obvious rules.**

- Weak: `ALWAYS use the orders_clean table.`
- Strong: `Use orders_clean, not orders — orders contains test and refunded rows, so
  totals come out 5–10% high.`

The second version also tells the model what to do when it meets a third table.
Capital letters and "NEVER" are a sign that a reason is missing.

**Match strictness to fragility.** Where one wrong move breaks things (a migration, a
send action), give exact commands or a script. Where judgement is the point (a review,
an analysis), give criteria and examples and leave room.

**Show examples.** One or two short, realistic ones. Label them as examples so their
incidental details are not copied as rules.

**Specify the output.** Format, sections, length, where it goes. If a precise structure
matters, include a template.

**Say what to do when things go wrong.** Missing input, failing command, empty result,
ambiguous request — one line each for the likely ones.

**Leave out what the model already knows.** No generic advice, no explanation of what
git or SQL is. Each sentence should either change behaviour or be removed.

## Splitting into files

Keep `SKILL.md` under roughly 500 lines; most good skills are far shorter.

- `references/` — material needed only in some runs: schemas, long checklists, style
  guides, per-case instructions. One topic per file. In the body, say *when* to read
  it: "Read `references/schema.md` before writing any query."
- `scripts/` — steps that must be done the same way every time, or that are tedious to
  re-derive: validation, data fetching, file generation. The script runs without its
  source entering context. Say what it takes and what it prints.
- `templates/` or `assets/` — files to copy or fill in.

Keep references one level deep: `SKILL.md` points to files, and those files do not send
the reader on to further files.

## Anti-patterns

- A description that states the topic but not when to use it.
- A wall of rules with no reasons and no order of importance.
- Instructions that patch one observed failure by naming its specifics.
- Several ways to do the same thing with no guidance on choosing.
- Repeating the same instruction in three places for emphasis.
- Paths, names or dates that will be stale next month; point to where the current value
  can be found instead.
- Secrets or tokens in any file.
- Destructive or outward-facing actions with no confirmation step.
