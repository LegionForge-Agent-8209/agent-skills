#!/usr/bin/env python3
"""Validate Agent Skills repository structure.

This lightweight validator checks the core structural rules from the
agentskills.io specification without external dependencies. It is intended for
fast local checks before running official reference validation tooling.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Any

NAME_RE = re.compile(r"^(?!-)(?!.*--)[a-z0-9-]{1,64}(?<!-)$")


def parse_scalar(value: str) -> str:
    """Parse a small YAML scalar subset used by SKILL.md frontmatter."""
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
        return value[1:-1]
    return value


def parse_frontmatter(text: str, path: Path) -> tuple[dict[str, Any], list[str]]:
    """Return frontmatter mapping and errors for a SKILL.md file.

    This intentionally supports the simple YAML subset commonly used for skill
    metadata: top-level `key: value` pairs and one-level mappings such as
    `metadata:` followed by indented `key: value` entries.
    """
    errors: list[str] = []
    if not text.startswith("---\n") and text != "---":
        return {}, [f"{path}: SKILL.md must start with YAML frontmatter delimiter '---'"]

    lines = text.splitlines()
    end_index = None
    for index, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            end_index = index
            break

    if end_index is None:
        return {}, [f"{path}: missing closing YAML frontmatter delimiter '---'"]

    metadata: dict[str, Any] = {}
    current_map: str | None = None
    for number, raw_line in enumerate(lines[1:end_index], start=2):
        if not raw_line.strip() or raw_line.lstrip().startswith("#"):
            continue

        if raw_line.startswith((" ", "\t")):
            if current_map is None:
                errors.append(f"{path}:{number}: indented value without parent mapping")
                continue
            if ":" not in raw_line:
                errors.append(f"{path}:{number}: expected 'key: value' in mapping")
                continue
            key, value = raw_line.strip().split(":", 1)
            metadata.setdefault(current_map, {})[key.strip()] = parse_scalar(value)
            continue

        current_map = None
        if ":" not in raw_line:
            errors.append(f"{path}:{number}: expected 'key: value'")
            continue

        key, value = raw_line.split(":", 1)
        key = key.strip()
        value = value.strip()
        if not key:
            errors.append(f"{path}:{number}: empty frontmatter key")
            continue
        if value == "":
            metadata[key] = {}
            current_map = key
        else:
            metadata[key] = parse_scalar(value)

    return metadata, errors


def validate_skill(skill_dir: Path) -> list[str]:
    errors: list[str] = []
    skill_file = skill_dir / "SKILL.md"

    if not skill_file.is_file():
        return [f"{skill_dir}: missing SKILL.md"]

    text = skill_file.read_text(encoding="utf-8")
    metadata, parse_errors = parse_frontmatter(text, skill_file)
    errors.extend(parse_errors)

    name = metadata.get("name")
    description = metadata.get("description")

    if not isinstance(name, str) or not name.strip():
        errors.append(f"{skill_file}: required frontmatter field 'name' is missing or empty")
    else:
        if name != skill_dir.name:
            errors.append(
                f"{skill_file}: name '{name}' must match parent directory '{skill_dir.name}'"
            )
        if not NAME_RE.match(name):
            errors.append(
                f"{skill_file}: name must be 1-64 chars, lowercase letters/numbers/hyphens only, "
                "with no leading, trailing, or consecutive hyphens"
            )

    if not isinstance(description, str) or not description.strip():
        errors.append(f"{skill_file}: required frontmatter field 'description' is missing or empty")
    elif len(description) > 1024:
        errors.append(f"{skill_file}: description is {len(description)} chars; maximum is 1024")

    compatibility = metadata.get("compatibility")
    if compatibility is not None:
        if not isinstance(compatibility, str) or not compatibility.strip():
            errors.append(f"{skill_file}: compatibility must be non-empty when provided")
        elif len(compatibility) > 500:
            errors.append(f"{skill_file}: compatibility is {len(compatibility)} chars; maximum is 500")

    allowed_tools = metadata.get("allowed-tools")
    if allowed_tools is not None and not isinstance(allowed_tools, str):
        errors.append(f"{skill_file}: allowed-tools must be a space-separated string when provided")

    metadata_field = metadata.get("metadata")
    if metadata_field is not None and not isinstance(metadata_field, dict):
        errors.append(f"{skill_file}: metadata must be a mapping when provided")

    return errors


def find_skill_dirs(root: Path) -> list[Path]:
    if (root / "SKILL.md").is_file():
        return [root]
    if not root.is_dir():
        return []
    return sorted(path for path in root.iterdir() if path.is_dir() and not path.name.startswith("."))


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate Agent Skills frontmatter and directory structure.")
    parser.add_argument(
        "path",
        nargs="?",
        default="skills",
        help="Skill directory or directory containing multiple skills (default: skills)",
    )
    args = parser.parse_args()

    root = Path(args.path)
    skill_dirs = find_skill_dirs(root)
    if not skill_dirs:
        print(f"No skill directories found under {root}", file=sys.stderr)
        return 2

    all_errors: list[str] = []
    for skill_dir in skill_dirs:
        all_errors.extend(validate_skill(skill_dir))

    if all_errors:
        print("Agent Skills validation failed:\n", file=sys.stderr)
        for error in all_errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(f"Validated {len(skill_dirs)} skill(s):")
    for skill_dir in skill_dirs:
        print(f"- {skill_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
