# Agent Skill authoring checklist

Use this checklist for a full publication review.

## Specification compliance

- [ ] Skill lives in a directory with a lowercase hyphenated name.
- [ ] Directory contains `SKILL.md` at its root.
- [ ] `SKILL.md` begins with YAML frontmatter delimited by `---`.
- [ ] Frontmatter includes required `name` and `description` fields.
- [ ] `name` exactly matches the parent directory name.
- [ ] `name` is 1-64 characters.
- [ ] `name` contains only lowercase letters, numbers, and hyphens.
- [ ] `name` does not start or end with a hyphen.
- [ ] `name` does not contain consecutive hyphens.
- [ ] `description` is non-empty and 1024 characters or fewer.
- [ ] Optional `compatibility`, if present, is 500 characters or fewer.

## Skill quality

- [ ] The skill captures real expertise, a repeated workflow, or a recurring agent correction.
- [ ] Scope is narrow enough to trigger precisely but broad enough to be useful.
- [ ] Description explains when to use the skill, not just what it is.
- [ ] Instructions focus on what the agent might not know without the skill.
- [ ] Generic best practices have been removed unless they are project-specific.
- [ ] Gotchas are concrete and actionable.
- [ ] Output formats are shown as templates when consistency matters.

## Progressive disclosure

- [ ] `SKILL.md` contains only always-needed instructions.
- [ ] Long references are moved into `references/`.
- [ ] The skill says when to read each reference file.
- [ ] Scripts are placed in `scripts/` and referenced with relative paths.
- [ ] Templates, examples, schemas, and static resources are placed in `assets/`.
- [ ] Referenced files exist.

## Script safety, if applicable

- [ ] Scripts are non-interactive.
- [ ] Scripts expose `--help` or document usage clearly.
- [ ] Inputs are accepted via flags, environment variables, files, or stdin.
- [ ] Structured data goes to stdout; diagnostics go to stderr.
- [ ] Error messages explain what went wrong and how to fix it.
- [ ] Destructive or stateful scripts support `--dry-run`, `--confirm`, or equivalent safeguards.
- [ ] Dependencies are documented or declared inline where possible.

## Publication readiness

- [ ] Local validation passes: `python3 scripts/validate_skills.py skills`.
- [ ] Official reference validation passes when available.
- [ ] License is clear at the repository and/or skill level.
- [ ] README or index lists the skill and its purpose.
- [ ] Known limitations are documented.
