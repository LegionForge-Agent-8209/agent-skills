---
name: agent-skill-authoring
description: Use this skill when creating, reviewing, or improving Agent Skills that follow the agentskills.io format. It helps draft compliant SKILL.md files, write precise activation descriptions, decide what belongs in scripts/references/assets, and validate skill naming/frontmatter before publishing.
license: MIT
compatibility: Works with agents that support the Agent Skills folder format and Markdown/YAML SKILL.md files.
metadata:
  author: JP Cruz
  version: "0.1.0"
---

# Agent Skill authoring

Use this skill to create or revise a portable Agent Skill. Optimize for a small, useful package that teaches the agent a reusable workflow it would otherwise perform inconsistently.

## Workflow

1. **Define the skill boundary**
   - Identify the repeated workflow, domain procedure, utility, or correction pattern the skill captures.
   - Prefer a coherent unit of work over a broad grab bag of advice.
   - Confirm the skill adds context the agent would not reliably know on its own.

2. **Choose the directory and name**
   - Create a lowercase hyphenated directory such as `code-review` or `pdf-processing`.
   - Set frontmatter `name` to exactly the same value as the directory.
   - Use only lowercase letters, numbers, and hyphens; avoid leading, trailing, or consecutive hyphens.

3. **Write activation-focused frontmatter**
   - Include required fields: `name` and `description`.
   - Keep `description` under 1024 characters.
   - Phrase the description as a trigger instruction: "Use this skill when...".
   - Mention user intents, related phrases, file types, systems, or workflows that should activate the skill.
   - Add optional `license`, `compatibility`, and `metadata` only when useful.

4. **Write concise operating instructions**
   - Keep `SKILL.md` focused on the steps needed every time the skill activates.
   - Include concrete procedures, checklists, output templates, gotchas, and validation loops.
   - Avoid generic advice the agent already knows.
   - Put long references, examples, schemas, and templates in separate files.

5. **Use progressive disclosure**
   - Place detailed docs in `references/` and tell the agent when to read each file.
   - Place reusable executable helpers in `scripts/` and document their command-line usage.
   - Place templates, examples, schemas, and static resources in `assets/`.
   - Reference files with paths relative to the skill root, for example `references/authoring-checklist.md`.

6. **Validate before publishing**
   - From this repository, run:
     ```bash
     python3 scripts/validate_skills.py skills
     ```
   - If official reference tooling is available, also run:
     ```bash
     skills-ref validate ./skills/<skill-name>
     ```
   - Fix all structural errors before publishing or copying the skill to another client.

## Recommended `SKILL.md` template

```markdown
---
name: skill-name
description: Use this skill when the agent needs to [perform workflow]. It helps with [specific capabilities] and should activate when the user mentions [triggering contexts].
license: MIT
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

## When to add support files

- Add `references/REFERENCE.md` when the skill needs detailed procedures that are not always relevant.
- Add `assets/` when the skill needs reusable templates, examples, sample config, schemas, or static media.
- Add `scripts/` when deterministic logic, validation, transformation, or repeated command sequences would be safer than model-only execution.

Read `references/authoring-checklist.md` when doing a full review of a skill before publication.
