# Skills

This directory contains publishable Agent Skills.

Each child directory is expected to be a standalone skill:

```text
skills/
└── skill-name/
    ├── SKILL.md
    ├── scripts/      # optional
    ├── references/   # optional
    └── assets/       # optional
```

Run validation from the repository root:

```bash
python3 scripts/validate_skills.py skills
```
