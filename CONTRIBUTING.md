# Contributing

1. One skill per folder: `skills/<name>/SKILL.md`, with `name` (equal to the folder) and `description` in YAML frontmatter.
2. Write original, practical guidance. Do not paste or translate third-party content; link official public sources under **Further reading**.
3. No private data: no personal names, company/client names, internal links, local paths or secrets.
4. Run `python3 scripts/validate_skills.py` and `python3 -m unittest discover -s tests` before opening a PR.
5. Add an entry to `CHANGELOG.md`.
