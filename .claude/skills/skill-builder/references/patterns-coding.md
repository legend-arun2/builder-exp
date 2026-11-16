# Pattern: coding-workflow skills

For skills that encode how work is done in a codebase: reviews, releases, adding a
component the house way, debugging playbooks, migrations.

## What makes these effective

- **Real commands, verified.** Run each command once before writing it down. A skill
  with a wrong test command fails on its first step.
- **Unwritten conventions.** The value is in what cannot be inferred from the code:
  which of two existing patterns is the preferred one, what reviewers reject.
- **A checkable definition of done.** "Tests pass and lint is clean" can be verified;
  "code is high quality" cannot.
- **Point at exemplars.** "Follow the structure of `src/api/users.ts`" stays current
  as the code changes; a pasted copy does not.
- **Stop points.** Say where to pause for the user (before pushing, before a schema
  change) and where not to.

## Skeleton

```markdown
# <Name>

<Goal: what a good outcome is, in one or two sentences.>

## Before starting
<Inputs to gather; state to check, e.g. clean working tree, right branch.>

## Steps
1. <Action, with the exact command where one exists.>
2. <Action. Reason, if not obvious.>
3. ...

## Conventions
- <Rule> — <reason>.
- Model new code on `<path to exemplar>`.

## Done when
- [ ] <Verifiable condition, with the command that verifies it>
- [ ] ...

## If something goes wrong
- <Likely failure> → <what to do>.

## Output
<What to report back, and in what form.>
```

## Example (abridged)

```markdown
---
name: add-endpoint
description: Adds a REST endpoint to the API service following the team's layering and test conventions. Use when the user asks to add, create or expose an endpoint, route or API method in `services/api`. Not for GraphQL resolvers or changes to the public SDK.
---

# Add an endpoint

A finished endpoint has a route, a handler, a service function, validation, and tests
at both the handler and service level, and passes `make check`.

## Steps
1. Read `services/api/src/routes/projects.ts` and its handler — new endpoints mirror it.
2. Add the request schema in `schemas/` first. Handlers trust validated input, so
   skipping this lets bad data reach the database.
3. Put business logic in `services/`, not in the handler — handlers are not unit-tested.
4. Add tests next to each file (`*.test.ts`).
5. Run `make check` (lint, types, tests; about a minute).

## Done when
- [ ] `make check` passes
- [ ] The route appears in `npm run routes`

## Output
List the files added or changed and paste the final line of `make check`.
```

## Script candidates

Scaffolding files from a template, collecting changed files or merged pull requests,
checking a naming convention.
