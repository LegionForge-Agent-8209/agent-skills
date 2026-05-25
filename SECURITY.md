# Security Policy

## Supported versions

| Version | Supported |
| --- | --- |
| Latest `master` | Yes |
| Older snapshots | No — use the latest revision |

## Reporting a vulnerability

**Do not open a public GitHub issue for security vulnerabilities.**

Report security issues to: security@legionforge.org

Include in your report:

- Description of the vulnerability
- Steps to reproduce
- Affected files or skills
- Suggested fix if you have one

You will receive an acknowledgement within 72 hours. Critical issues should be fixed or mitigated as quickly as practical, with coordinated disclosure preferred.

## Security controls

This repository follows LegionForge dev-rig principles proportionally for a Markdown + small-Python Agent Skills registry.

| Control | Tool | Where |
| --- | --- | --- |
| Skill structure validation | `scripts/validate_skills.py` | CI (`validate.yml`) + local |
| Unit tests | `unittest` | CI (`validate.yml`) + local |
| Trigger-eval syntax checks | `python3 -m json.tool` | CI (`validate.yml`) + local |
| Secret scanning | gitleaks via `LegionForge/dev-rig` | CI (`security.yml`) + pre-commit |
| Static analysis | Semgrep + CodeQL via `LegionForge/dev-rig` | CI (`security.yml`) |
| Local file hygiene | pre-commit hooks | `.pre-commit-config.yaml` |
| Python lint/security hooks | ruff + bandit | `.pre-commit-config.yaml` |

## Current audit / SBOM posture

The shared LegionForge dev-rig `audit.yml` and `sbom.yml` workflows assume an installable Python package with dependency metadata. This repository currently has no runtime package or third-party runtime dependencies; it is primarily Markdown, JSON examples, tests, and standard-library Python scripts.

If this repository later adds a `pyproject.toml`, packaged helpers, or third-party dependencies, add dependency CVE scanning and SBOM generation using the dev-rig reusable workflows before release.

## Security-sensitive content rules

Skills and support files must not contain:

- API keys, tokens, passwords, private keys, or credential-store exports
- private repository URLs or host aliases unless intentionally public
- passphrase paths, SSH fingerprints, or internal backup artifact names
- raw user memories, conversation contents, documents, or unredacted logs
- commands that push private data to public repositories

Security-sensitive workflows, such as Thoth memory backups, must default to privacy-preserving behavior and require explicit user consent before handling secrets, plaintext archives, or destructive cleanup.
