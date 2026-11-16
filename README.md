# builder-exp

## skill-forge

A Claude Code skill for creating and improving other skills. It lives in
`.claude/skills/skill-forge/` and is available in any session opened on this repo.

**It runs only when you call it.** Type `/skill-forge`, optionally followed by what you
want. It never starts on its own, even if you ask for a skill in plain words.

- `/skill-forge a skill that drafts our release notes`
- `/skill-forge turn what we just did into a skill`
- `/skill-forge .claude/skills/weekly-metrics isn't triggering — fix it`

**What it does:** interviews you about the skill, picks a pattern (coding workflow,
data and analysis, or tool integration), drafts it, runs a structural check, tests it
on three realistic prompts in a fresh context, and refines it from the results.

**Layout**

| Path | Purpose |
|---|---|
| `SKILL.md` | The workflow |
| `references/interview.md` | Questions to ask before drafting |
| `references/writing-guide.md` | How to write descriptions and instructions that work |
| `references/patterns-*.md` | Skeleton and example per skill type |
| `references/testing.md` | How to test and refine |
| `templates/SKILL.template.md` | Starting point for a new skill |
| `scripts/validate_skill.py` | Structural check |

Run the check on any skill folder:

```bash
python3 .claude/skills/skill-forge/scripts/validate_skill.py .claude/skills/<skill-name>
```
