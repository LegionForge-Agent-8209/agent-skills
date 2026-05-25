---
name: thoth-memory-backup-to-github
description: Use this skill when a user wants to design, create, review, or troubleshoot a backup workflow for Thoth memory and local Thoth state to a private GitHub repository. It helps inventory Thoth data under the user's data directory, exclude secrets and volatile files, create encrypted backup archives, validate restore readiness, and document a safe GitHub-based retention process without exposing private data.
license: MIT
compatibility: Designed for standard Thoth installations where durable data lives under ~/.thoth or THOTH_DATA_DIR. Requires user-approved shell/Git operations and a private GitHub repository. Encryption tooling may vary by platform.
metadata:
  author: "LegionForge Agent - Jeli2 directed by jp@legionforge.org"
  version: "0.1.0"
---

# Thoth memory backup to GitHub

Use this skill to help a Thoth user build a safe, general-purpose backup workflow for Thoth memory and local state using a **private GitHub repository**. Prefer encrypted archives, explicit restore validation, and documented retention over raw plaintext syncs.

This skill generalizes lessons from real Thoth backup workflows, but it must not assume any private instance labels, repository names, SSH aliases, host paths, passphrase files, schedules, or operational scripts.

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
