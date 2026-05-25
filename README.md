# Agent Skills

A public collection of reusable [Agent Skills](https://agentskills.io/) for AI agents.

This repository is intended to publish practical skills and utilities we use in real workflows so others can copy, adapt, and improve them.

## What is an Agent Skill?

An Agent Skill is a lightweight folder-based package that teaches an AI agent a reusable capability, workflow, or domain-specific procedure.

At minimum, each skill is a directory containing a `SKILL.md` file with YAML frontmatter and Markdown instructions:

```text
skill-name/
└── SKILL.md
```

Skills can also include optional support files:

```text
skill-name/
├── SKILL.md      # Required: metadata + instructions
├── scripts/      # Optional: executable helpers
├── references/   # Optional: deeper documentation loaded on demand
├── assets/       # Optional: templates, examples, schemas, images, etc.
└── ...
```

## Repository layout

```text
.
├── README.md
├── CONTRIBUTING.md
├── LICENSE
├── scripts/
│   └── validate_skills.py
└── skills/
    ├── agent-skill-authoring/
    │   ├── SKILL.md
    │   ├── assets/
    │   ├── references/
    │   └── scripts/
    └── thoth-memory-backup-to-github/
        ├── SKILL.md
        ├── assets/
        └── references/
```

- `skills/` contains publishable Agent Skills.
- `scripts/validate_skills.py` performs local structural validation before publishing.
- Each child directory under `skills/` should be a complete skill whose folder name matches the `name` in `SKILL.md`.

## Authorship convention

Skills created in this repository should use the following frontmatter metadata author unless a specific skill has a documented reason to differ:

```yaml
metadata:
  author: "LegionForge Agent - Jeli2 directed by jp@legionforge.org"
```

This records that the published skill was agent-authored under JP's direction rather than solely hand-authored.

## Provenance and quality process

Skills in this repository may be drafted, reviewed, or revised by Jeli2, a Thoth-based AI assistant directed by JP Cruz. Published skills are intended to come from real workflows, repeated agent corrections, or operational runbooks rather than generic prompt templates.

Before publication, skills should be reviewed for:

- structural compatibility with the Agent Skills folder format
- trigger-description precision and near-miss behavior
- safety, privacy, and licensing risks
- existence and usefulness of referenced support files
- removal or generalization of private instance details
- local validation and tests

Pull requests and pushes to `master` run GitHub Actions validation for skill structure, unit tests, and trigger-eval JSON syntax. Security workflows also run dev-rig-backed gitleaks secret scanning plus Python/script SAST on pushes, pull requests, a weekly schedule, and manual dispatch.

## CI/CD and security posture

This repository follows LegionForge dev-rig principles proportionally for a Markdown + small-Python Agent Skills registry:

- `validate.yml` runs skill structure validation, unit tests, and trigger-eval JSON parsing.
- `security.yml` uses `LegionForge/dev-rig` reusable workflows for gitleaks secret scanning and Python/script SAST.
- `.pre-commit-config.yaml` provides local hygiene, JSON/YAML checks, ruff, bandit, and gitleaks hooks.
- `SECURITY.md` documents vulnerability reporting and the current security controls.

The shared dev-rig dependency-audit and SBOM workflows assume an installable Python package. This repo currently has no packaged runtime dependencies, so those workflows are deferred until a `pyproject.toml` or third-party dependency surface is introduced.

## Current skills

| Skill | Purpose |
| --- | --- |
| [`agent-skill-authoring`](skills/agent-skill-authoring/SKILL.md) | Helps agents draft, review, and validate Agent Skills that follow the agentskills.io specification. |
| [`thoth-memory-backup-to-github`](skills/thoth-memory-backup-to-github/SKILL.md) | Helps design, review, and validate encrypted Thoth memory/local-state backups to a user's private GitHub repository. |

## Validating skills

Run the local validator:

```bash
python3 scripts/validate_skills.py skills
```

The validator checks the core published specification rules:

- each skill directory contains `SKILL.md`
- `SKILL.md` has YAML frontmatter
- required `name` and `description` fields exist
- `name` matches the parent directory
- `name` uses lowercase letters, numbers, and hyphens only
- `description` is non-empty and no more than 1024 characters
- optional `compatibility` is no more than 500 characters

For full compatibility testing, also validate with the official reference tooling when available:

```bash
skills-ref validate ./skills/agent-skill-authoring
skills-ref validate ./skills/thoth-memory-backup-to-github
```

## Installing a skill in a compatible client

Agent Skills are portable folders. Depending on your client, you can usually copy a skill folder into the client's skills directory.

For example, VS Code looks for project skills under `.agents/skills/`:

```bash
mkdir -p .agents/skills
cp -R skills/agent-skill-authoring .agents/skills/
cp -R skills/thoth-memory-backup-to-github .agents/skills/
```

Then restart or refresh the agent session and confirm the skill appears in the client's skills list.

## Authoring principles

When adding skills to this repository:

1. Start from real workflow experience, runbooks, scripts, or repeated agent corrections.
2. Keep `SKILL.md` focused on the instructions needed every time the skill activates.
3. Move detailed references, examples, templates, and long procedures into `references/` or `assets/`.
4. Use scripts when repeated logic should be deterministic, testable, or safer than asking the model to improvise.
5. Use the repository authorship convention in each skill's `metadata.author` frontmatter.
6. Validate the skill before publishing.

## License

This repository is licensed under the MIT License. See [`LICENSE`](LICENSE).

Individual skills may include their own `license` frontmatter if a different license applies to that skill.
