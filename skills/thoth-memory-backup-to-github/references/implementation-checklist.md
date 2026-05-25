# Thoth memory backup implementation checklist

Use this checklist before creating or modifying a user's backup workflow.

## Scope and consent

- [ ] User confirmed the Thoth data directory (`$THOTH_DATA_DIR` or `~/.thoth`).
- [ ] User confirmed the GitHub repository exists or approved creating/initializing one.
- [ ] User confirmed the GitHub repository is private.
- [ ] User selected SSH or HTTPS Git authentication.
- [ ] User selected an encryption method.
- [ ] User understands where the decryption key/passphrase is stored and how it will be recovered.
- [ ] User approved any file writes, shell commands, commits, and pushes required by the environment.

## Data classification

- [ ] Memory database identified, usually `memory.db`.
- [ ] Memory vector directory identified, usually `memory_vectors/`.
- [ ] Conversations/threads storage identified if included.
- [ ] Workflows/tasks storage identified if included.
- [ ] Wiki vault path identified if included.
- [ ] Documents/uploads identified if included.
- [ ] Plugin/custom-tool metadata identified if included.
- [ ] Logs/caches/browser/session data excluded unless explicitly requested.
- [ ] Secret/auth/token locations excluded by default.

## SQLite safety

- [ ] Live database files are copied with SQLite backup API or Thoth is stopped first.
- [ ] SQLite integrity check is planned for restored copies.
- [ ] WAL/SHM sidecars are not relied on when online backup is used.
- [ ] Backup manifest records whether SQLite backup or raw copy was used.

## Encryption and archive safety

- [ ] Unencrypted staging directory is outside the Git repo or ignored.
- [ ] Archive is encrypted before it is moved into the Git repo.
- [ ] `.gitignore` blocks raw archives, staging directories, unencrypted database files, temp files, and accidental `.thoth` copies.
- [ ] Large encrypted artifacts are split or kept below GitHub file-size limits.
- [ ] Manifest does not contain secrets.
- [ ] Unencrypted staging files are removed only after encrypted archive and validation succeed.

## GitHub safety

- [ ] Remote URL points to the intended private repository.
- [ ] No unencrypted Thoth data appears in `git status`.
- [ ] No files larger than GitHub's standard limit are staged unless Git LFS was explicitly chosen.
- [ ] Commit message does not reveal private details.
- [ ] Push is explicitly approved by the user.

## Restore validation

- [ ] Newest archive decrypts in a temporary directory.
- [ ] Expected files exist after extraction.
- [ ] `memory.db` opens with SQLite if present.
- [ ] `PRAGMA integrity_check` returns `ok` for SQLite databases when possible.
- [ ] Split parts reassemble if splitting is used.
- [ ] Restore validation does not overwrite a live Thoth data directory.
- [ ] Restore drill result is documented.

## Automation readiness

- [ ] Manual backup path succeeded first.
- [ ] Manual restore validation succeeded first.
- [ ] Scheduled job has failure notifications.
- [ ] Scheduled job has logs that do not reveal secrets.
- [ ] Local retention does not delete the only successful artifact before Git commit/push is verified.
- [ ] Automation has a dry-run or status command.
