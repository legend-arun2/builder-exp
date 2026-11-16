# builder-exp

## skill-builder

A Claude Code skill for creating and improving other skills. It lives in
`.claude/skills/skill-builder/` and is available in any session opened on this repo.

**Use it** by typing `/skill-builder`, optionally followed by what you want, or just
ask in plain words:

- "Create a skill that drafts our release notes"
- "Turn what we just did into a skill"
- "My weekly-metrics skill isn't triggering — fix it"

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
python3 .claude/skills/skill-builder/scripts/validate_skill.py .claude/skills/<skill-name>
```
