# Interview question bank

Pick the questions whose answers you do not already have. Ask two to four at a time,
in plain language, and offer options where the user may not know what is possible.
Prefer asking for a real example over asking for a description: "show me the last
release note you wrote" yields more than "what should release notes contain?".

## Core questions (every skill)

**Purpose**
- What should this skill let you do that is slow, error-prone or inconsistent today?
- How often does this come up? (If it is a one-off, a skill is the wrong tool — just do
  the task.)

**Triggering**
- What would you actually type when you want this? Give two or three phrasings.
- Is there a similar-sounding request that should *not* use this skill?
- Should it also start on its own when relevant, or only when you invoke it by name?

**Result**
- What does a good result look like? Is there an existing example to copy?
- Where should the result go — chat reply, a file (which path), a pull request, a tool?
- How long or detailed should it be? Who reads it?

**Inputs and needs**
- What does it start from — a file, a branch, a ticket, a date range, nothing?
- Which tools, commands, credentials or data does it need?

**Pitfalls**
- When this was done before (by you, a colleague, or Claude), what went wrong?
- Is there anything it must never do, or must always ask before doing?

**Scope**
- Just this project, or all your projects?

## Coding-workflow skills

- Which commands build, test, lint and run the project? Which are slow or flaky?
- What conventions are not written down anywhere (naming, layout, error handling,
  commit style, branch names)?
- What is the definition of done — tests green, lint clean, docs updated, changelog?
- Which files or directories are off-limits or generated?
- What do reviewers most often push back on?
- Are there steps that need a human decision in the middle?

## Data and analysis skills

- Where does the data live (warehouse, files, API) and which SQL dialect or library?
- Which tables or files matter, and which look right but must not be used?
- How exactly are the key metrics defined? Any filters that are always applied
  (test accounts, internal users, time zone, currency)?
- What are the known data-quality traps (late-arriving rows, duplicates, changed
  definitions on a certain date)?
- How do you sanity-check a number before trusting it?
- What form does the answer take — a number, a table, a chart, a written summary?

## Tool-integration skills

- Which tools or services are involved, and are they already connected in this
  environment (MCP server, CLI, API key)?
- Which actions only read, and which create, change, send or delete?
- Which of those actions need your confirmation every time?
- Which identifiers does it need (workspace, project, database, channel) and where do
  they come from?
- What should happen when the tool is unavailable, returns nothing, or rate-limits?
- Is there a naming or formatting convention for what it creates?

## When the user is unsure

If the user cannot answer a question, propose a sensible default, say it is a default,
and move on. Record open questions and revisit them after the first test run — seeing
a real output usually makes the answer obvious.
