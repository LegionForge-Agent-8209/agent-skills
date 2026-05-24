# Agent Skill authoring checklist

Use this checklist for a full publication review.

## Intake review

- [ ] The skill is based on a real workflow, runbook, correction pattern, artifact, or repeated user need.
- [ ] The source of truth is named or summarized.
- [ ] The intended trigger contexts are clear.
- [ ] Near-miss tasks that should not trigger the skill are identified.
- [ ] Environment requirements are known or explicitly absent.
- [ ] Safety, privacy, and licensing constraints are known.

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
- [ ] Optional `license`, if present, is a short license name or bundled license-file reference.
- [ ] Optional `compatibility`, if present, is non-empty and 500 characters or fewer.
- [ ] Optional `metadata`, if present, is a key-value mapping.
- [ ] Optional `allowed-tools`, if present, is a space-separated string and marked experimental in user-facing docs when appropriate.

## Skill quality rubric

Score each category 0-2 before publication:

| Category | 0 | 1 | 2 |
| --- | --- | --- | --- |
| Specificity | Generic advice | Some project/domain detail | Concrete workflow details the agent would otherwise miss |
| Trigger precision | Vague or broad | Mostly clear | Clear should-trigger and should-not-trigger boundary |
| Scope | Too broad/narrow | Usable but fuzzy | Coherent reusable unit of work |
| Progressive disclosure | Everything in `SKILL.md` | Some split-out files | Always-needed content only in `SKILL.md`, references loaded on demand |
| Executability | Scripts/commands unclear | Mostly runnable | Commands/scripts documented, deterministic, non-interactive |
| Validation | No checks | Manual checks only | Structural validation plus task-specific review/evals |
| Safety | Risks unstated | Risks noted | Destructive/private/security-sensitive steps are gated or excluded |

Publication target: no category below 1, and at least four categories scoring 2.

## Description and trigger evaluation

- [ ] Description starts with or implies "Use this skill when...".
- [ ] Description focuses on user intent, not implementation internals.
- [ ] Description includes relevant file types, systems, workflows, or user phrases.
- [ ] Description avoids generic phrasing such as "helps with" alone.
- [ ] Description does not overreach into adjacent skills.
- [ ] Description is under 1024 characters after edits.
- [ ] At least 8 should-trigger eval prompts exist.
- [ ] At least 8 should-not-trigger eval prompts exist.
- [ ] Negative evals include near-misses with overlapping keywords.
- [ ] Eval prompts include realistic wording: typos, file paths, terse requests, and context-heavy requests.
- [ ] Failures are addressed by changing general trigger categories, not by keyword-stuffing exact eval text.

## Skill quality

- [ ] The skill captures real expertise, a repeated workflow, or a recurring agent correction.
- [ ] Scope is narrow enough to trigger precisely but broad enough to be useful.
- [ ] Description explains when to use the skill, not just what it is.
- [ ] Instructions focus on what the agent might not know without the skill.
- [ ] Generic best practices have been removed unless they are project-specific.
- [ ] Gotchas are concrete and actionable.
- [ ] Output formats are shown as templates when consistency matters.
- [ ] Defaults are selected where multiple tools or approaches exist.
- [ ] Fragile operations are prescriptive; flexible operations explain intent and constraints.

## Progressive disclosure

- [ ] `SKILL.md` contains only always-needed instructions.
- [ ] `SKILL.md` is comfortably under 500 lines.
- [ ] Long references are moved into `references/`.
- [ ] The skill says when to read each reference file.
- [ ] Scripts are placed in `scripts/` and referenced with relative paths.
- [ ] Templates, examples, schemas, and static resources are placed in `assets/`.
- [ ] Referenced files exist.
- [ ] References do not create a deep chain of nested documents.

## Script safety, if applicable

- [ ] Scripts are non-interactive.
- [ ] Scripts expose `--help` or document usage clearly.
- [ ] Inputs are accepted via flags, environment variables, files, or stdin.
- [ ] Structured data goes to stdout; diagnostics go to stderr.
- [ ] Error messages explain what went wrong and how to fix it.
- [ ] Scripts are idempotent where practical.
- [ ] Inputs are validated rather than guessed.
- [ ] Destructive or stateful scripts support `--dry-run`, `--confirm`, or equivalent safeguards.
- [ ] Large outputs are summarized, paginated, or written to files by default.
- [ ] Dependencies are documented, pinned, or declared inline where possible.

## Safety and publication review

- [ ] No secrets, tokens, private emails, private URLs, or internal credentials are included.
- [ ] Private project details are generalized or removed before public release.
- [ ] License is clear at the repository and/or skill level.
- [ ] Third-party assets, examples, or copied snippets are licensed for reuse.
- [ ] Destructive operations require explicit confirmation or are documented as manual-only.
- [ ] Network access requirements are disclosed in `compatibility` when relevant.
- [ ] The skill does not request broader tool permissions than it needs.

## Publication readiness

- [ ] Local validation passes: `python3 scripts/validate_skills.py skills`.
- [ ] Official reference validation passes when available.
- [ ] README or index lists the skill and its purpose.
- [ ] Known limitations are documented.
- [ ] Version metadata is updated if the skill is being revised.
