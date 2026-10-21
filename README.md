# UX Skills Toolbox

Agent skills (Claude Code / Codex `SKILL.md` format) for product designers.

| Skill | What it covers |
|---|---|
| `project-kickoff` | Kickoff: briefing, heuristic/competitor/accessibility diagnosis, personas, first validated delivery |
| `product-evolution` | Initiatives, rationale, opportunity trees, fake doors, design QA, rituals, growth design |
| `ux-research` | Research briefs, methods, interviews, JTBD, synthesis and prioritization |
| `ux-strategy` | Strategy stack, PMF/ICP, SaaS metrics, MVP, avoiding the feature trap |
| `tv-motion` | Motion & focus for 10-foot TV UIs on low-end Android TV / Fire TV devices |

## Install
```bash
./install.sh --claude   # ~/.claude/skills
./install.sh --codex    # ~/.codex/skills
./install.sh --agents   # ~/.agents/skills
```

## Validate & test
```bash
python3 scripts/validate_skills.py
python3 -m unittest discover -s tests
```

## Contributing
See [CONTRIBUTING.md](CONTRIBUTING.md).

## License
[MIT](LICENSE)
