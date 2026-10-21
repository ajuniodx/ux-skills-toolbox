#!/usr/bin/env python3
"""Validate skills/*/SKILL.md frontmatter and scan the repo for private data."""
import pathlib, re, sys

BANNED = re.compile(
    r"(?i)\b(tray|lwsa|locaweb|bivo\w*|junotv|coram|mi stick|vespasiano|pampulha|obsidian)\b"
    r"|/Users/|~/Workspace|notion\.site|figma\.com/file|docs\.google\.com|drive\.google\.com|bit\.ly"
    r"|\b(sk-|rnk-|ghp_)[A-Za-z0-9]"
)
SKIP = {".git", "tests", "__pycache__"}


def validate(root):
    root = pathlib.Path(root)
    errors = []
    skills = sorted(root.glob("skills/*/SKILL.md"))
    if not skills:
        errors.append("no skills found")
    for p in skills:
        t = p.read_text(encoding="utf-8")
        m = re.match(r"^---\n(.*?)\n---\n", t, re.S)
        if not m:
            errors.append(f"{p.relative_to(root)}: missing frontmatter")
            continue
        fm = dict(l.split(":", 1) for l in m.group(1).splitlines() if ":" in l)
        if fm.get("name", "").strip() != p.parent.name:
            errors.append(f"{p.relative_to(root)}: name must equal folder '{p.parent.name}'")
        if len(fm.get("description", "").strip()) < 20:
            errors.append(f"{p.relative_to(root)}: description too short")
    for p in root.rglob("*"):
        rel = p.relative_to(root)
        if not p.is_file() or SKIP & set(rel.parts) or p.name == "validate_skills.py":
            continue
        for i, line in enumerate(p.read_text(errors="ignore").splitlines(), 1):
            if BANNED.search(line):
                errors.append(f"{rel}:{i}: private/banned reference")
    return len(skills), errors


if __name__ == "__main__":
    n, errs = validate(sys.argv[1] if len(sys.argv) > 1 else pathlib.Path(__file__).resolve().parent.parent)
    print("\n".join(errs) or f"OK: {n} skills valid")
    sys.exit(1 if errs else 0)
