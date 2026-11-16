# Testing and refining a drafted skill

The aim is to find out, cheaply, whether the skill triggers on the right requests and
whether a session that knows nothing else produces the right result.

## 1. Write three prompts with the user

- **Two that should trigger.** Make them sound like the user on a normal day: casual
  wording, incomplete detail, real file or table names. One typical case and one that
  is harder (missing input, an edge case from the interview's pitfalls).
- **One near-miss that should not trigger.** A request that shares vocabulary with the
  skill but belongs elsewhere.

Avoid prompts that restate the skill ("use the release-notes skill to follow its
steps"). They pass regardless and reveal nothing.

For each should-trigger prompt, write one or two lines on what a good result contains,
taken from the success criteria in the interview. Agree these before running anything,
so the judgement is not bent to fit the output.

## 2. Check triggering

Read the description as if it were the only thing known about the skill, next to each
prompt:

- Would this description clearly claim each should-trigger prompt? Are the prompt's
  key words, or close synonyms, in it?
- Would it leave the near-miss alone? If not, tighten the wording or add a "Not for…"
  clause.

Full confirmation comes only from real use in a later session, since skills are
discovered at session start. Say this to the user rather than claiming it is verified.

## 3. Run the should-trigger prompts in a fresh context

A fresh context is essential: the session that wrote the skill already knows the
user's intent and will fill gaps without noticing them.

**With a subagent available:** start one per prompt, giving it only:

> Read the skill at `<path>/SKILL.md` and follow it to handle this request:
> "<prompt>". Work in `<a scratch directory or the real project, as appropriate>`.
> At the end, report what you did, anything in the skill that was unclear or missing,
> and any step you skipped and why.

Do not add hints or context beyond what a real session would have.

**Without one:** tell the user that the test is weaker, then reread the skill from the
top as a newcomer, following it literally for each prompt and noting every point
where you rely on knowledge that is not written in the skill.

**Side effects:** if the skill writes to external tools, sends messages, deploys or
deletes, do not let the test perform those actions for real. Run up to the write step
and inspect what would be sent, or use a sandbox target the user names.

## 4. Review

Show the user each output next to its expected result. Look at:

- **Result** — does it meet the agreed criteria? Right format and place?
- **Process** — were steps skipped, reordered or misread? Was time wasted on something
  the skill told it to do that did not help?
- **Gaps reported** — anything the tester found unclear or had to guess.

The user's reaction outranks the checklist. Ask what they would change.

## 5. Refine and rerun

Apply the cause-based fixes from step 6 of `SKILL.md`, rerun only the prompts affected,
and run the validator again. Stop when the user is satisfied or two rounds bring no
improvement.

## 6. Record what was tested

In the hand-over, list the prompts used, the outcome of each, and what was not tested
(real triggering in a new session, write actions, unusual inputs). If the user wants to
keep the prompts for later changes, save them as `tests/prompts.md` in the skill folder.
