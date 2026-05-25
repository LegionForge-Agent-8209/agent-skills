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

- Auth method: SSH / HTTPS / GitHub CLI / other
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

## Automation

- Schedule:
- Notification channel:
- Failure behavior:
- Dry-run/status command:
- Logs location:

## Open questions

- [ ]
- [ ]
- [ ]
