# Contributing Agent Skills

Thanks for improving this Agent Skills collection.

## Skill requirements

Each skill must be a directory under `skills/` containing a `SKILL.md` file:

```text
skills/
└── my-skill/
    └── SKILL.md
```

The `SKILL.md` file must start with YAML frontmatter:

```markdown
---
name: my-skill
description: Use this skill when the agent needs to ...
metadata:
  author: "LegionForge Agent - Jeli2 directed by jp@legionforge.org"
---

Markdown instructions go here.
```

## Authorship convention

Skills created in this repository should use this metadata author value unless a specific skill has a documented reason to differ:

```yaml
metadata:
  author: "LegionForge Agent - Jeli2 directed by jp@legionforge.org"
```

This records the agent-directed authorship model for published skills.

## Naming rules

The `name` value must:

- match the parent directory name exactly
- be 1-64 characters
- use lowercase letters, numbers, and hyphens only
- not start or end with a hyphen
- not contain consecutive hyphens

Good names:

- `agent-skill-authoring`
- `code-review`
- `pdf-processing`

Avoid:

- `AgentSkillAuthoring`
- `agent_skill_authoring`
- `-agent-skill`
- `agent--skill`

## Description guidance

Descriptions drive skill activation. A good description should explain both:

1. what the skill does
2. when the agent should use it

Prefer:

```yaml
description: Use this skill when creating or reviewing Agent Skills. It helps draft compliant SKILL.md files, choose focused descriptions, structure references and scripts, and validate naming/frontmatter rules.
```

Avoid:

```yaml
description: Helps with skills.
```

## Recommended structure

```text
my-skill/
├── SKILL.md
├── scripts/       # Optional deterministic helpers
├── references/    # Optional detailed docs loaded on demand
└── assets/        # Optional templates, examples, schemas, images
```

Keep `SKILL.md` concise and move long supporting material into referenced files.

## Validation checklist

Before opening a pull request or publishing a skill:

```bash
python3 scripts/validate_skills.py skills
python3 -m unittest discover -s tests
```

GitHub Actions runs these checks on pushes and pull requests to `master`, along with JSON syntax validation for trigger-eval assets. Security workflows also run dev-rig-backed gitleaks secret scanning and Python/script SAST.

For local QC, install pre-commit when available:

```bash
pre-commit install
pre-commit run --all-files
```

The local pre-commit configuration is adapted from LegionForge dev-rig for this repository's Markdown, JSON, YAML, and small Python-script surface.

Then manually review:

- [ ] The skill came from a real workflow, not generic filler.
- [ ] `description` clearly identifies trigger conditions.
- [ ] `metadata.author` uses `LegionForge Agent - Jeli2 directed by jp@legionforge.org` unless intentionally documented otherwise.
- [ ] `SKILL.md` body gives concrete procedures, examples, or gotchas.
- [ ] Any referenced files exist and use relative paths from the skill root.
- [ ] Referenced files are substantive, not empty placeholders or stubs.
- [ ] Source notes identify when external assumptions should be re-checked.
- [ ] Scripts are non-interactive and provide `--help` where practical.
- [ ] Destructive scripts have dry-run or explicit confirmation safeguards.
- [ ] Licensing is clear before publishing.

## Pull request format

Include:

- summary of the skill or change
- source workflow or problem it addresses
- validation command output
- any compatibility requirements
- known limitations or follow-up work
