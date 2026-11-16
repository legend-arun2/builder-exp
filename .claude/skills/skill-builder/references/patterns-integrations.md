# Pattern: tool-integration skills

For skills that drive external tools: MCP servers (Notion, GitHub, Vercel, Canva…),
command-line tools, or HTTP APIs.

## What makes these effective

- **Check the tools are there first.** Tool availability differs between sessions. The
  first step verifies the needed tools or CLI are present and stops with a clear message
  if not, instead of improvising a substitute.
- **Exact tool names and the order to call them.** Name the tools as they appear
  (e.g. `mcp__Notion__notion-search`) and give the sequence: find → read → change →
  verify. Leave the parameters to the tool's own schema unless one is easy to get wrong.
- **Separate reading from writing.** Reading is free. Anything that creates, changes,
  sends, publishes or deletes is listed explicitly, with which of those need the user's
  confirmation. Things sent to other people cannot be taken back.
- **Identifiers come from somewhere.** State how to find the workspace, project or
  database: ask once, look it up by name, or read it from a config file. Do not
  hard-code identifiers that differ per user; never store secrets in the skill.
- **Verify after writing.** Read the object back or report its link, so success is
  observed and not assumed.
- **Plan for failure.** Not found, permission denied, rate limit, partial success in a
  batch. For batches, say whether to stop or continue and how to report what was done.

## Skeleton

```markdown
# <Name>

<Goal: what ends up where, in one or two sentences.>

## Requires
- <Tools / CLI / connection>. If missing, tell the user what to connect and stop.

## Inputs
- <Identifier> — <how to obtain it>.

## Steps
1. Find: <tool> to locate <thing>. If several match, ask which.
2. Read: <tool> to get current state.
3. Prepare the change and show it to the user. <Confirmation rule.>
4. Write: <tool>.
5. Verify: <tool>, then report the link.

## Actions that need confirmation
- <Action> — <why>.

## Conventions
- <Naming, formatting, labels for created objects.>

## If something goes wrong
- <Failure> → <action>.

## Output
<What to report: what changed, links, anything skipped.>
```

## Example (abridged)

```markdown
---
name: ship-log
description: Records a deployed release as a page in the team's Notion "Ship Log" database, with the merged pull requests and the deployment link. Use when the user asks to log a release, update the ship log, or record what was deployed. Not for writing release notes for customers.
---

# Ship log entry

## Requires
- Notion tools (`mcp__Notion__*`) and GitHub tools (`mcp__github__*`). If either is
  missing, say which and stop.

## Steps
1. Find the database with `mcp__Notion__notion-search` for "Ship Log". If there is
   more than one result, ask which.
2. List pull requests merged since the previous entry's date with
   `mcp__github__list_pull_requests`.
3. Draft the entry (title `YYYY-MM-DD <version>`, one line per pull request with its
   link) and show it. Creating the page notifies the whole team, so wait for a yes.
4. Create it with `mcp__Notion__notion-create-pages`.
5. Fetch the new page to confirm it exists and reply with its link.

## If something goes wrong
- No pull requests since the last entry → say so and do not create an empty page.
```

## Script candidates

Calling an API that has no tool, reshaping a tool's output, batch operations that need
a resumable record of what has been done.
