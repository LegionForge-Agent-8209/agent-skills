# Thoth memory backup plan

## Ownership

- User / owner:
- Date created:
- Last reviewed:
- Backup repository URL:
- Repository visibility: private

## Thoth environment

- Operating system:
- Thoth installation type: installer / source checkout / Docker / other
- Thoth data directory:
- `THOTH_DATA_DIR` set: yes / no
- Thoth must be stopped for backup: yes / no / unknown
- Thoth instance age / usage level:
- Custom memory/storage modifications: none / yes / unknown
- Modification notes:

## Memory audit

- Audit date:
- Audit method:
- `memory.db` exists: yes / no / unknown
- `memory.db` size:
- Entity/memory count:
- Relation count:
- `memory_vectors/` exists: yes / no / unknown
- `memory_vectors/` size:
- Wiki vault enabled/path/status:
- Recent memory/dream-cycle errors:
- Audit limitations:

## Preflight decisions

- Backup profile: memory-only / Thoth continuity / full-private-forensic
- GitHub account ready: yes / no
- Private backup repository verified: yes / no / unknown
- Git authentication method: SSH / HTTPS / GitHub CLI / other
- Run mode: on demand / scheduled / both
- Manual backup validated before automation: yes / no
- Plaintext GitHub push explicitly approved: no / yes / not applicable

## Backup scope

### Include

- [ ] `memory.db`
- [ ] `memory_vectors/`
- [ ] conversations / threads
- [ ] workflows / tasks
- [ ] documents / uploads
- [ ] wiki vault
- [ ] settings metadata
- [ ] plugin/custom-tool metadata
- [ ] other:

### Profile notes

- Memory-only rationale:
- Continuity rationale:
- Full/private forensic rationale and explicit consent:

### Exclude by default

- [ ] API keys and provider tokens
- [ ] OAuth/session tokens
- [ ] SSH keys
- [ ] browser profile/session data
- [ ] logs unless explicitly needed
- [ ] caches/temp files
- [ ] local model weights
- [ ] raw unencrypted `.thoth` copy

## Encryption

- Tool/method:
- Recipient/public key or passphrase location:
- Recovery procedure:
- Rotation procedure:
- Unattended key/passphrase handling, if scheduled:
- Plaintext/local-only test notes, if encryption is declined:
- Risk acknowledgement:

## Archive and manifest

- Archive naming pattern:
- Split size, if any:
- Manifest location:
- Manifest fields:
  - timestamp
  - source data directory
  - included paths
  - excluded paths
  - SQLite backup status
  - archive files
  - checksums
  - tool versions

## Git workflow

- Branch:
- Commit message pattern:
- Push policy:
- GitHub retention policy:
- Local retention policy:

## Restore validation

- Temporary restore directory:
- Decryption command:
- Extraction command:
- SQLite integrity command:
- Last successful validation:
- Known limitations:
- Restore goal: memory-only / continuity / migration / future-agent setup / other
- Expected restore operator: user / future agent / both

## Automation

- Schedule:
- Idle-window requirement:
- Notification channel:
- Approval requirement before push:
- Failure behavior:
- Dry-run/status command:
- Logs location:

## Open questions

- [ ]
- [ ]
- [ ]
