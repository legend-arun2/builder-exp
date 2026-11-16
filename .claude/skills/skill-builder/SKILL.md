---
name: skill-builder
description: Creates new Claude Code skills and improves existing ones through an interview, draft, validate, test and refine workflow. Use when the user asks to create, build or write a skill, to turn a workflow or the current conversation into a skill, to improve or debug an existing skill, or says a skill is not triggering or not being followed. Covers coding-workflow, data-analysis and tool-integration skills. Not for one-off tasks that will never repeat, or for hooks, settings and CLAUDE.md edits.
argument-hint: "[what the skill should do | path to an existing skill]"
---

# Skill Builder

Build a skill that triggers when it should, stays out of the way when it should not, and
produces the result the user actually wants. Skills fail in three common ways, and every
step below exists to prevent one of them:

- **It never triggers** — the description does not match how the user really asks.
- **It is bloated** — everything is in one file, so the important instructions get diluted.
- **It is followed badly** — it lists rules without reasons, so they are applied rigidly
  in the wrong situations or dropped under pressure.

## Choose the mode

- **Create** — the user wants a new skill. Run steps 1–7.
- **Improve** — the user points at an existing skill, or reports that one misbehaves.
  Read the whole skill folder, ask what goes wrong (get a concrete prompt and what
  happened), then run steps 4–7. Reread `references/writing-guide.md` before editing.

All paths below are relative to this skill's folder.

## 1. Capture intent

Check the conversation first. If the user says "turn this into a skill", the workflow
is already there: extract the steps taken, the tools used, the corrections the user made
(these are the most valuable part — they are what a fresh session would get wrong), and
the shape of the final output. Then confirm your summary instead of re-asking.

Otherwise interview the user with `references/interview.md`. Ask two to four questions
at a time, skip anything already answered, and stop when you can state all of these:

1. What the skill does, in one sentence.
2. The phrases the user would really type that should trigger it, and one similar
   request that should not.
3. What a good result looks like (format, location, level of detail).
4. What it needs: tools, files, commands, credentials, data sources.
5. Known pitfalls — what goes wrong when this is done without guidance.

Do not draft before item 2 and item 3 are concrete. A vague trigger gives a skill that
never fires; a vague success criterion gives one that cannot be tested.

## 2. Classify and pick a pattern

Decide which type fits best and read only that file:

| Type | Typical requests | Read |
|---|---|---|
| Coding workflow | repo conventions, reviews, releases, debugging playbooks | `references/patterns-coding.md` |
| Data and analysis | recurring queries, metric definitions, reports | `references/patterns-data.md` |
| Tool integration | driving MCP tools, APIs or CLIs | `references/patterns-integrations.md` |

A skill that spans two types takes its skeleton from the dominant one and borrows
sections from the other.

Then decide:

- **Name** — lowercase words joined by hyphens, short, describes the action
  (`release-notes`, `weekly-metrics`). The folder name must equal the name.
- **Location** — `.claude/skills/<name>/` in the current project by default, so it is
  versioned with the code. Use `~/.claude/skills/<name>/` only if the user wants it in
  every project.
- **Extra files** — plan a `references/` file for any block that is long or needed only
  in some runs, and a `scripts/` file for any step that must be done identically every
  time. A skill with neither is fine.

## 3. Draft

Read `references/writing-guide.md`, then copy `templates/SKILL.template.md` to the new
skill folder as `SKILL.md` and fill it in. The points that matter most:

- **Description** — written in third person; says what the skill does, then when to use
  it with the user's own trigger phrases, then what it is not for. This one field decides
  whether the skill is ever loaded, so spend real effort on it.
- **Body** — imperative steps in the order they happen. Give the reason for every rule
  that is not obvious; a reason lets the model handle cases the rule did not foresee.
- **Examples** — one or two short, realistic input → output examples beat a paragraph
  of description.
- **Output** — state the exact format and where the result goes.
- **Size** — keep `SKILL.md` focused on what every run needs. Move the rest to
  `references/` and say in the body exactly when to read each file.

Write only what a capable model would not already know or would get wrong. Every line
of generic advice ("write clean code", "be careful") weakens the lines that matter.

## 4. Validate

Run the structural check and fix every error; consider each warning:

```bash
python3 <this-skill-folder>/scripts/validate_skill.py <new-skill-folder>
```

It checks the frontmatter, name, description, size, file references and leftover
template placeholders. It cannot judge whether the skill is any good — that is step 5.

## 5. Test

Read `references/testing.md` and follow it. In short: agree three realistic prompts with
the user (two that should trigger, one near-miss that should not), run each
should-trigger prompt in a fresh context that has only the skill and the prompt, and
review the results against the success criteria from step 1.

Testing in the same context that wrote the skill proves little, because that context
already knows what the user wants. Use a subagent when one is available; if not, say so
and do a careful read-through as a newcomer instead.

## 6. Refine

For each problem found, find the cause before editing:

- **Did not trigger / triggered wrongly** → fix the description.
- **Step skipped or done wrong** → the instruction is unclear, buried, or lacks its
  reason. Rewrite or move it; do not just add "IMPORTANT".
- **Output shape wrong** → add or sharpen the output format or an example.
- **Wasted effort** → cut the instruction that caused it.

Generalise from the failure. A patch that names the exact test case ("if the file is
called report.csv…") passes the test and fails in real use. Also remove anything the
test showed to be unnecessary — a skill should get shorter as often as it gets longer.

Rerun the affected prompt, and rerun the validator. Stop when the user is satisfied, or
after two rounds with no improvement — then report what still fails instead of looping.

## 7. Hand over

Tell the user, briefly:

- where the skill is and which files it has;
- how to invoke it (`/<name>`, or the phrases that trigger it);
- what was tested and how it went, and what was not tested;
- that a new skill is normally picked up in the next session, and that it must be
  committed to be shared or kept.

Do not commit or push unless the user asks.
