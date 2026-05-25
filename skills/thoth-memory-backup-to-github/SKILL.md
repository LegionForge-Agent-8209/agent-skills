---
name: thoth-memory-backup-to-github
description: Use this skill when a user wants to design, create, review, or troubleshoot a backup workflow for Thoth memory and local Thoth state to a private GitHub repository. It helps inventory Thoth data under the user's data directory, exclude secrets and volatile files, create encrypted backup archives, validate restore readiness, and document a safe GitHub-based retention process without exposing private data.
license: MIT
compatibility: Designed for standard Thoth installations where durable data lives under ~/.thoth or THOTH_DATA_DIR. Requires user-approved shell/Git operations and a private GitHub repository. Encryption tooling may vary by platform.
metadata:
  author: "LegionForge Agent - Jeli2 directed by jp@legionforge.org"
  version: "0.2.0"
---

# Thoth memory backup to GitHub

Use this skill to help a Thoth user build a safe, general-purpose backup workflow for Thoth memory and local state using a **private GitHub repository**. Prefer encrypted archives, explicit restore validation, and documented retention over raw plaintext syncs.

This skill generalizes lessons from real Thoth backup workflows, but it must not assume any private instance labels, repository names, SSH aliases, host paths, passphrase files, schedules, or operational scripts.

## Setup questionnaire

Run this questionnaire before designing or implementing the backup workflow. Ask the user to answer what they can, and explicitly mark unknowns rather than guessing. If the user only wants a high-level plan, collect the questionnaire in prose. If the user wants implementation help, use the answers to choose a safe backup scope, encryption approach, GitHub workflow, and restore-validation path.

### 1. Thoth age, size, and memory audit

1. How long have you been running this Thoth instance?
2. Roughly how heavily have you used memory? For example, do you expect more than 100 memories/entities, large documents, or long conversation history?
3. Can Thoth run a memory audit/status check and share the non-secret output here? Useful audit output includes:
   - memory/entity count
   - relation count
   - memory database path and size
   - memory vector directory path and size
   - wiki vault enabled/path/status, if relevant
   - recent memory/dream-cycle errors, if any
4. If an audit cannot be run, ask the user to say why: no tool access, remote system, permission issue, Thoth unavailable, or unknown.

### 2. Installation and data directory

1. What operating system and installation style are you using: Windows installer, macOS app, Linux installer, source checkout, Docker/container, or other?
2. Is `THOTH_DATA_DIR` set? If yes, what path does it point to?
3. If `THOTH_DATA_DIR` is not set, should the workflow assume the standard data directory such as `~/.thoth`?
4. Is Thoth running continuously while backups will run, or can it be stopped during backup windows?
5. Is the backup being run from inside the same machine/container where Thoth stores its data?

### 3. Memory-system modifications and compatibility risks

Ask whether the user has modified Thoth in ways that could make a standard memory backup risky. Examples:

1. Have you altered the memory system programmatically?
2. Have you edited Thoth files related to memory, knowledge graph, embeddings, wiki export, dream cycle, document extraction, or conversation storage?
3. Have you moved memory storage to another database, vector store, external service, symlinked directory, mounted volume, or custom architecture?
4. Have you changed `memory.py`, `knowledge_graph.py`, `documents.py`, `wiki_vault.py`, embedding configuration, or related storage modules?
5. Are there multiple Thoth instances sharing one data directory or one GitHub backup repository?
6. Are there custom plugins, Custom Tools, MCP servers, or scripts that write directly to memory files?

If the answer to any compatibility question is yes or unknown, pause implementation and first produce a risk assessment plus a custom inventory plan.

### 4. GitHub readiness

This skill assumes the user is comfortable enough with GitHub to maintain a **private** backup repository. If not, walk the user through the missing prerequisites before implementing backup scripts. Ask:

1. Do you already have a GitHub account?
2. Do you already have a private repository for Thoth backups?
3. Do you want the assistant/agent to help create or initialize the repository?
4. Which Git authentication method should be used: SSH key, HTTPS token/credential helper, GitHub CLI, or another method?
5. If using an agent or bot identity, has it been granted access only to the backup repository?
6. Are you comfortable with Git basics such as clone, commit, push, remote, and branch?
7. Should the skill include a beginner path for account creation, private repo creation, SSH/HTTPS setup, and first push validation?

Never proceed as if a repository is private unless the user confirms it or tooling verifies it.

### 5. Backup timing and automation preference

1. Should this backup run on demand, on a schedule, or both?
2. If scheduled, what frequency is appropriate: daily, weekly, before upgrades, after large memory imports, or another cadence?
3. Should scheduled backups run only when Thoth is idle?
4. Should failures notify the user through desktop, Discord/Telegram/Slack, email, or another channel?
5. Should the workflow require approval before each push, or should a fully unattended encrypted backup be allowed after setup?

### 6. Encryption preference and risk acknowledgement

1. This skill strongly recommends encrypted backups before Git. Are encrypted backups acceptable?
2. Which encryption method do you prefer or already use: `age`, `gpg`, OpenSSL, encrypted zip/7z, platform vault tooling, or another method?
3. How will the key/passphrase be stored for manual use?
4. If unattended scheduled backups are desired, where will the automation read the key/passphrase from, and what file permissions or OS secret store will protect it?
5. How will you recover the key/passphrase if the original machine is lost?
6. If the user prefers plain archives, stop and explain that plaintext Thoth backups may expose private memories, documents, conversations, provider metadata, and operational details. Continue only after explicit acknowledgement and preferably restrict plaintext to a local-only test, not GitHub.

### 7. Backup scope and exclusions

1. Is the goal memory-only backup or broader Thoth continuity backup?
2. Should the backup include documents/uploads, wiki vault, workflows/tasks, conversations, settings, plugins, Custom Tools, or channel configuration metadata?
3. Should logs be excluded, included for troubleshooting, or retained only locally?
4. Should browser profiles, OAuth/session data, API keys, provider tokens, SSH keys, and other runnable secrets be excluded? Default to exclude.
5. Are local model files or caches present, and should they be excluded to keep GitHub backup size reasonable?
6. Are there files too sensitive even for encrypted GitHub storage?

### 8. Restore expectations

1. What does success mean: recover only memories, recover Thoth continuity, migrate to a new machine, or clone a standard setup for future agents?
2. Should restore validation be a dry restore into a temporary folder, never overwriting the live Thoth directory?
3. How often should restore drills be performed?
4. Who is expected to perform restores: the user, a future agent, or both?
5. What documentation should be generated for a human to recover the backup without this exact chat context?

### 9. Retention, size, and governance

1. How many backup versions should remain locally?
2. How many backup versions should remain in GitHub history?
3. Are there GitHub file-size concerns requiring split archives or Git LFS?
4. Should old backup artifacts be pruned automatically only after a successful push and restore validation?
5. Are there legal, employer, customer, family, or personal privacy constraints on storing this data in GitHub, even encrypted?

After the questionnaire, summarize the answers as **Assumptions**, **Risks**, **Decisions needed**, and **Recommended next step** before creating scripts or running backup commands.

## Core principles

1. **Private repo only** — never recommend publishing Thoth memory or app state to a public repository.
2. **Encrypt before Git** — commit encrypted archives or encrypted split parts, not raw `~/.thoth` contents.
3. **Do not back up runnable secrets by default** — API keys, OAuth tokens, provider tokens, channel tokens, SSH keys, and browser sessions require explicit user consent and separate handling.
4. **Use online SQLite backup when possible** — for live Thoth databases, prefer SQLite's backup API or stop Thoth before copying database files.
5. **Exclude volatile sidecars** — do not archive SQLite `-wal` / `-shm` sidecars when an online database backup is used.
6. **Validate every backup path with a dry restore** — a backup workflow is incomplete until the user can inspect or restore the newest archive in a temporary directory.
7. **Document assumptions** — record data directory, repo URL, encryption method, retention policy, restore test date, and known exclusions.

## Intake questions

Ask only the questions needed for the current step:

1. What Thoth data directory should be backed up? Default to `$THOTH_DATA_DIR` when set, otherwise `~/.thoth`.
2. Is the GitHub repository already created, and is it private?
3. Should backups use SSH or HTTPS authentication?
4. Which encryption tool is available or preferred: `age`, `gpg`, OpenSSL, encrypted zip/7z, or another tool?
5. Where should the encryption passphrase/key live, and how will the user recover it if the machine is lost?
6. Should the backup include only memory/knowledge data or broader Thoth state such as workflows, documents, wiki vault, plugins, and settings?
7. What should be excluded: logs, browser profile, caches, provider metadata, channel data, documents, local model files, or secrets?
8. What retention policy should GitHub and local disk use?

## Workflow

1. **Confirm official Thoth assumptions**
   - Standard Thoth durable data is local-first and stored under `~/.thoth` or a platform/data-directory equivalent.
   - The official memory database path is `~/.thoth/memory.db` unless `THOTH_DATA_DIR` changes it.
   - Memory vectors live under `~/.thoth/memory_vectors/`.
   - Provider keys and subscription tokens should live in the OS credential store when available; do not assume they are safe to copy as files.
   - Read `references/thoth-source-notes.md` before making claims about standard Thoth paths or modules.

2. **Inventory the user's local state**
   - Identify `THOTH_DATA_DIR` or default to `~/.thoth`.
   - List top-level files/directories without printing secret contents.
   - Classify data into:
     - memory/knowledge data
     - conversation/workflow/settings state
     - documents/wiki exports
     - credentials/secrets/auth state
     - caches/logs/browser/session data
   - Use `assets/backup-plan-template.md` to capture the resulting plan.

3. **Design a safe backup set**
   - Include memory-critical files such as `memory.db` and `memory_vectors/` when present.
   - Consider including conversations, workflows/tasks, wiki vault, documents, settings, and plugin/custom-tool metadata only after explaining privacy and size tradeoffs.
   - Exclude secrets and high-risk auth material by default.
   - Exclude caches and transient files unless the user explicitly wants a full forensic snapshot.
   - Warn that GitHub has file-size limits; split large encrypted archives or use Git LFS only after discussing tradeoffs.

4. **Create a robust snapshot procedure**
   - Prefer staging a temporary snapshot directory outside the Git working tree.
   - For SQLite databases, use Python `sqlite3.Connection.backup()` or stop Thoth before raw copying.
   - Copy selected non-database files with metadata-preserving tools where available.
   - Create a manifest with timestamp, source data directory, included paths, excluded paths, SQLite backup status, archive file names, and tool versions.
   - Encrypt the staged snapshot before moving it into the backup repository.
   - Remove unencrypted staging files after successful encryption and validation.

5. **Store in a private GitHub repository**
   - Verify the remote repository is private before pushing if tool access allows.
   - Use a repo-local `.gitignore` that blocks unencrypted archives, staging directories, temp files, and accidental raw `.thoth` copies.
   - Commit only encrypted artifacts, manifests that do not reveal secrets, restore drill docs, and operational scripts.
   - Push only after explicit user approval.

6. **Validate restore readiness**
   - Decrypt the newest archive into a temporary restore directory.
   - Confirm expected files exist, especially `memory.db` when memory backup is in scope.
   - Run SQLite integrity checks on copied databases when `sqlite3` is available.
   - Confirm archive parts reassemble when splitting is used.
   - Do not restore over a live Thoth data directory during validation.
   - Document restore test results and any limitations.

7. **Automate carefully**
   - Use scheduled workflows or OS cron/systemd only after the manual path works.
   - Store passphrases/keys using OS secret storage when available; if a passphrase file is used for unattended operation, require restrictive permissions and document recovery risk.
   - Add notifications for backup failure, validation failure, and push failure.
   - Keep local retention small if GitHub is the history store, but never delete the only successful local artifact before a verified commit/push.

## Recommended support files

When creating a backup repo for a user, generate or maintain these files there:

```text
README.md                    # Purpose, scope, restore overview
.gitignore                   # Prevent raw/temporary/private data commits
scripts/create-backup.*      # Snapshot -> encrypt -> manifest
scripts/validate-latest.*    # Dry restore and integrity checks
scripts/backup-status.*      # Repo health, latest backup, file-size checks
docs/RESTORE_DRILL.md        # Human-readable restore validation process
backups/                     # Encrypted archives or split encrypted parts
manifests/                   # Non-secret manifests
```

Prefer scripts only when the user approves file creation in the backup repo. If the current task is only planning, produce a plan and do not write files.

## Safety checks before acting

Before running commands or creating scripts, confirm:

- the user knows this is for a **private** GitHub repository
- encryption is selected or the user explicitly accepts the risk of an unencrypted local-only test
- secrets are excluded unless the user explicitly requests a separate secret-backup process
- destructive cleanup has a dry-run or delayed deletion path
- restore validation will happen before considering the backup successful

## Private-workflow details to remove when generalizing

Do not copy or assume:

- private repository names or paths
- private instance labels
- organization-specific SSH aliases, keys, fingerprints, or passphrase paths
- container-specific paths from one user's environment
- exact backup artifact names from prior private workflows
- schedules, retention counts, or operational policies unless the current user chooses them

Generalize those into placeholders such as `<backup-repo>`, `<thoth-data-dir>`, `<encryption-recipient>`, and `<retention-policy>`.

## Output format

When designing or reviewing a backup workflow, respond with:

```markdown
## Backup scope
- Data directory:
- Included:
- Excluded:

## Privacy and encryption
- Repository visibility:
- Encryption method:
- Secret handling:

## Proposed workflow
1. Snapshot
2. Encrypt
3. Validate
4. Commit/push
5. Retention

## Restore validation
- Dry-restore steps:
- Integrity checks:
- Last verified:

## Next actions
- [ ] ...
```

Read `references/implementation-checklist.md` before implementing scripts, and use `assets/backup-plan-template.md` when drafting a persistent plan.
