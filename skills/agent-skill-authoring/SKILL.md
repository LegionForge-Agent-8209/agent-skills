---
name: agent-skill-authoring
description: Use this skill when creating, reviewing, or improving Agent Skills that follow the agentskills.io format. It helps draft compliant SKILL.md files, write precise activation descriptions, test trigger behavior, scaffold skill folders, decide what belongs in scripts/references/assets, and validate naming/frontmatter before publishing.
license: MIT
compatibility: Works with agents that support the Agent Skills folder format and Markdown/YAML SKILL.md files. Optional scaffold helper requires Python 3.9+.
metadata:
  author: JP Cruz
  version: "0.2.0"
---

# Agent Skill authoring

Use this skill to create or revise a portable Agent Skill. Optimize for a small, useful package that teaches the agent a reusable workflow it would otherwise perform inconsistently.

## Intake questions

Before drafting a new skill, collect the smallest useful context set:

1. What repeated workflow, runbook, correction pattern, or utility should this skill capture?
2. What real task, repository, incident, conversation, or artifact is the source of truth?
3. What user phrases, files, systems, or intents should trigger the skill?
4. What near-miss prompts should **not** trigger the skill?
5. What environment assumptions exist: tools, languages, system packages, network access, credentials, or client compatibility?
6. What should the agent produce: code, report, review, transformed files, commands, checklist, or another output format?
7. What safety/privacy/licensing constraints apply, especially for destructive actions, credentials, private data, or public publication?

If the user only provides a broad idea, ask 2-4 targeted questions instead of fabricating domain details.

## Workflow

1. **Define the skill boundary**
   - Identify the repeated workflow, domain procedure, utility, or correction pattern the skill captures.
   - Prefer a coherent unit of work over a broad grab bag of advice.
   - Confirm the skill adds context the agent would not reliably know on its own.
   - Write down one sentence describing what is explicitly out of scope.

2. **Choose the directory and name**
   - Create a lowercase hyphenated directory such as `code-review` or `pdf-processing`.
   - Set frontmatter `name` to exactly the same value as the directory.
   - Use only lowercase letters, numbers, and hyphens; avoid leading, trailing, or consecutive hyphens.
   - Use `scripts/scaffold_skill.py` when creating a new skill directory from scratch.

3. **Write activation-focused frontmatter**
   - Include required fields: `name` and `description`.
   - Keep `description` under 1024 characters.
   - Phrase the description as a trigger instruction: "Use this skill when...".
   - Mention user intents, related phrases, file types, systems, or workflows that should activate the skill.
   - Add optional `license`, `compatibility`, `allowed-tools`, and `metadata` only when useful.
   - Include `compatibility` only when there are real environment requirements.

4. **Write concise operating instructions**
   - Keep `SKILL.md` focused on the steps needed every time the skill activates.
   - Include concrete procedures, checklists, output templates, gotchas, and validation loops.
   - Avoid generic advice the agent already knows.
   - Put long references, examples, schemas, and templates in separate files.
   - Calibrate control: be prescriptive for fragile sequences; give freedom when multiple valid approaches exist.

5. **Use progressive disclosure**
   - Place detailed docs in `references/` and tell the agent when to read each file.
   - Place reusable executable helpers in `scripts/` and document their command-line usage.
   - Place templates, examples, schemas, and static resources in `assets/`.
   - Reference files with paths relative to the skill root, for example `references/authoring-checklist.md`.

6. **Test the trigger description**
   - Draft 8-10 prompts that should trigger the skill and 8-10 near-miss prompts that should not.
   - Include casual phrasing, typos, file paths, implicit intent, and context-heavy prompts.
   - Use `assets/example-trigger-evals.json` as a starter format.
   - If should-trigger prompts are missed, broaden the description by intent category.
   - If should-not-trigger prompts activate it, tighten the boundary or clarify exclusions.
   - Do not overfit by copying exact eval wording into the description.

7. **Validate before publishing**
   - From this repository, run:
     ```bash
     python3 scripts/validate_skills.py skills
     ```
   - If official reference tooling is available, also run:
     ```bash
     skills-ref validate ./skills/<skill-name>
     ```
   - Read `references/authoring-checklist.md` for a full publication review.
   - Fix all structural errors before publishing or copying the skill to another client.

## Available scripts

- `scripts/scaffold_skill.py` — Creates a compliant starter skill directory with `SKILL.md`, optional `scripts/`, `references/`, and `assets/` folders, and safe frontmatter defaults.

Example from the repository root:

```bash
python3 skills/agent-skill-authoring/scripts/scaffold_skill.py \
  --skills-root skills \
  --name release-watch \
  --description "Use this skill when monitoring software releases and summarizing relevant changes for a repository or package." \
  --author "JP Cruz" \
  --license MIT \
  --with-references \
  --with-assets
```

## Support file decision table

| Need | Put it in |
| --- | --- |
| Always-needed workflow steps | `SKILL.md` |
| Long domain notes or detailed runbooks | `references/` |
| Templates, examples, schemas, sample data | `assets/` |
| Deterministic validation, transformation, or scaffolding | `scripts/` |
| Commands likely to be mistyped | `scripts/` |
| Rarely needed edge-case detail | `references/` with clear load conditions |

## Anti-patterns

Avoid skills that:

- merely restate generic LLM best practices without domain or workflow specifics
- are too broad to trigger precisely, such as `software-engineering`
- are too narrow to reuse, such as `rename-one-specific-file`
- put huge reference material directly in `SKILL.md`
- rely on unstated environment assumptions
- include scripts that prompt interactively or block waiting for input
- use vague descriptions like "Helps with data"
- present many equal tool options instead of choosing a default and noting exceptions
- claim compatibility or tool permissions that have not been tested
- include private data, secrets, or project-confidential context in public skills

## Recommended `SKILL.md` template

```markdown
---
name: skill-name
description: Use this skill when the agent needs to [perform workflow]. It helps with [specific capabilities] and should activate when the user mentions [triggering contexts].
license: MIT
compatibility: Requires [only include if true].
metadata:
  author: your-name-or-org
  version: "0.1.0"
---

# Skill title

One short paragraph describing what the skill does and the outcome it helps produce.

## Workflow

1. First concrete step.
2. Second concrete step.
3. Validation or review step.

## Gotchas

- Non-obvious issue the agent should know before acting.
- Environment-specific convention or constraint.

## Output format

Use this format when responding:

```markdown
## Summary
...

## Details
...
```
```

Read `references/authoring-checklist.md` when doing a full review of a skill before publication.
