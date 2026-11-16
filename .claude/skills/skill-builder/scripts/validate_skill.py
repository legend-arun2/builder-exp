#!/usr/bin/env python3
"""Structural check for a Claude Code skill folder.

Usage: validate_skill.py <skill-folder>

Prints errors and warnings. Exits 0 when there are no errors, 1 when there are,
2 on bad usage. Standard library only.
"""

import re
import sys
from pathlib import Path

NAME_MAX = 64
DESC_MAX = 1024
DESC_MIN = 60
BODY_WARN_LINES = 500
NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
PLACEHOLDER_RE = re.compile(r"\{\{.*?\}\}")
# Relative paths into the skill's own sub-folders, e.g. references/schema.md
REF_RE = re.compile(r"(?<![\w/.-])((?:references|scripts|templates|assets|tests)/[\w./-]*\w)")
TRIGGER_CUES = ("use when", "use this", "use for", "use to", "when the user", "when asked", "triggers")
KNOWN_KEYS = {
    "name", "description", "argument-hint", "allowed-tools", "disable-model-invocation",
    "user-invocable", "model", "license", "metadata", "context", "agent", "hooks",
    "when_to_use", "paths", "effort",
}


def split_frontmatter(text):
    """Return (frontmatter_lines, body) or (None, text) when there is no frontmatter."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None, text
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            return lines[1:i], "\n".join(lines[i + 1:])
    return None, text


def parse_frontmatter(lines):
    """Parse the simple YAML used in skill frontmatter: top-level `key: value`,
    quoted values, and `>` / `|` block scalars or indented continuation lines."""
    data, problems = {}, []
    key, parts, style = None, [], None

    def flush():
        if key is not None:
            joiner = "\n" if style == "|" else " "
            data[key] = joiner.join(p for p in parts if p != "" or style == "|").strip()

    for raw in lines:
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        if raw[0] in " \t":
            if key is None:
                problems.append(f"unexpected indented line in frontmatter: {raw.strip()!r}")
            else:
                parts.append(raw.strip())
            continue
        m = re.match(r"^([A-Za-z0-9_-]+):(?:\s+(.*))?$", raw.rstrip())
        if not m:
            problems.append(f"cannot parse frontmatter line: {raw.strip()!r}")
            continue
        flush()
        key, value = m.group(1), (m.group(2) or "").strip()
        parts, style = [], None
        if re.fullmatch(r"[>|][+-]?", value):
            style = value[0]
        elif len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            parts.append(value[1:-1])
        else:
            if key == "description" and re.search(r":\s", value):
                problems.append(
                    "description contains ': ' but is not quoted; YAML may misread it. "
                    "Wrap it in double quotes or use a '>' block."
                )
            parts.append(value)
    flush()
    return data, problems


def validate(skill_dir):
    errors, warnings = [], []
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.is_file():
        return [f"{skill_md} not found (the file must be named exactly SKILL.md)"], warnings

    text = skill_md.read_text(encoding="utf-8")
    fm_lines, body = split_frontmatter(text)
    if fm_lines is None:
        return ["SKILL.md must start with a frontmatter block delimited by '---' lines"], warnings

    fm, problems = parse_frontmatter(fm_lines)
    errors.extend(problems)

    # name
    name = fm.get("name", "")
    if not name:
        errors.append("frontmatter is missing 'name'")
    else:
        if not NAME_RE.match(name):
            errors.append(f"name {name!r} must be lowercase letters, digits and single hyphens")
        if len(name) > NAME_MAX:
            errors.append(f"name is {len(name)} characters; the limit is {NAME_MAX}")
        if name != skill_dir.name:
            errors.append(f"name {name!r} does not match the folder name {skill_dir.name!r}")

    # description
    desc = fm.get("description", "")
    if not desc:
        errors.append("frontmatter is missing 'description'")
    else:
        if len(desc) > DESC_MAX:
            errors.append(f"description is {len(desc)} characters; the limit is {DESC_MAX}")
        if len(desc) < DESC_MIN:
            warnings.append(
                f"description is only {len(desc)} characters; say what the skill does "
                "and when to use it, with the user's own phrases"
            )
        low = desc.lower()
        if not any(cue in low for cue in TRIGGER_CUES):
            warnings.append("description does not say when to use the skill (e.g. 'Use when ...')")
        if re.search(r"\b(I|my|you|your)\b", desc):
            warnings.append("description should be in the third person (avoid I / you)")
        if "<" in desc or ">" in desc:
            warnings.append("description contains angle brackets; remove them")

    for k in fm:
        if k not in KNOWN_KEYS:
            warnings.append(f"unrecognised frontmatter field {k!r} (check the spelling)")

    # placeholders
    found = sorted(set(PLACEHOLDER_RE.findall(text)))
    if found:
        shown = ", ".join(found[:3]) + (" ..." if len(found) > 3 else "")
        errors.append(f"SKILL.md still contains {len(found)} template placeholder(s): {shown}")

    # body
    body_lines = [ln for ln in body.splitlines()]
    if not body.strip():
        errors.append("SKILL.md has no instructions after the frontmatter")
    elif len(body_lines) > BODY_WARN_LINES:
        warnings.append(
            f"SKILL.md body is {len(body_lines)} lines (over {BODY_WARN_LINES}); "
            "move situational material into references/"
        )

    # referenced files
    for ref in sorted(set(REF_RE.findall(body))):
        if "*" in ref or "<" in ref:
            continue
        if not (skill_dir / ref).exists():
            errors.append(f"SKILL.md refers to {ref!r}, which does not exist in the skill folder")

    # unreferenced files (helps catch forgotten pointers)
    for sub in ("references", "scripts", "templates", "assets"):
        d = skill_dir / sub
        if d.is_dir():
            for f in sorted(p for p in d.rglob("*") if p.is_file()):
                if "__pycache__" in f.parts:
                    continue
                rel = f.relative_to(skill_dir).as_posix()
                if rel not in body:
                    warnings.append(f"{rel} is never mentioned in SKILL.md, so it will not be used")

    return errors, warnings


def main(argv):
    if len(argv) != 2 or argv[1] in ("-h", "--help"):
        print(__doc__.strip())
        return 2
    skill_dir = Path(argv[1]).resolve()
    if skill_dir.name == "SKILL.md":
        skill_dir = skill_dir.parent
    if not skill_dir.is_dir():
        print(f"ERROR: {skill_dir} is not a folder")
        return 2

    errors, warnings = validate(skill_dir)
    for e in errors:
        print(f"ERROR: {e}")
    for w in warnings:
        print(f"WARN:  {w}")
    if errors:
        print(f"\n{skill_dir.name}: {len(errors)} error(s), {len(warnings)} warning(s)")
        return 1
    print(f"{skill_dir.name}: OK" + (f" with {len(warnings)} warning(s)" if warnings else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
