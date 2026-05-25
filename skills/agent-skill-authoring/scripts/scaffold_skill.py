#!/usr/bin/env python3
"""Create a starter Agent Skill directory.

The generated skill follows the agentskills.io folder convention and writes a
minimal SKILL.md with required frontmatter. The script is intentionally
non-interactive so agents can run it safely from instructions.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Iterable

NAME_RE = re.compile(r"^(?!-)(?!.*--)[a-z0-9-]{1,64}(?<!-)$")
DEFAULT_AUTHOR = "LegionForge Agent - Jeli2 directed by jp@legionforge.org"


class ScaffoldError(Exception):
    """Raised when scaffold input or filesystem state is invalid."""


def validate_name(name: str) -> None:
    if not NAME_RE.match(name):
        raise ScaffoldError(
            "skill name must be 1-64 characters, lowercase letters/numbers/hyphens only, "
            "with no leading, trailing, or consecutive hyphens"
        )


def yaml_scalar(value: str) -> str:
    """Return a YAML-safe double-quoted scalar.

    JSON string syntax is a valid subset of YAML double-quoted scalar syntax for
    the strings this script emits. Using the standard library avoids incomplete
    hand-rolled escaping for newlines, tabs, quotes, backslashes, and other
    control characters.
    """

    return json.dumps(value, ensure_ascii=False)


def parse_metadata_items(items: Iterable[str]) -> list[tuple[str, str]]:
    metadata: list[tuple[str, str]] = []
    for item in items:
        if "=" not in item:
            raise ScaffoldError(f"metadata must use key=value format: {item!r}")
        key, value = item.split("=", 1)
        key = key.strip()
        if not key:
            raise ScaffoldError(f"metadata key cannot be empty: {item!r}")
        if any(char.isspace() for char in key) or ":" in key:
            raise ScaffoldError(f"metadata key must not contain whitespace or ':': {key!r}")
        metadata.append((key, value.strip()))
    return metadata


def build_skill_md(args: argparse.Namespace) -> str:
    metadata_items = parse_metadata_items(args.metadata)
    lines = ["---", f"name: {args.name}", f"description: {yaml_scalar(args.description)}"]

    if args.license:
        lines.append(f"license: {yaml_scalar(args.license)}")
    if args.compatibility:
        lines.append(f"compatibility: {yaml_scalar(args.compatibility)}")
    if args.allowed_tools:
        lines.append(f"allowed-tools: {yaml_scalar(args.allowed_tools)}")

    metadata_lines: list[str] = []
    if args.author:
        metadata_lines.append(f"  author: {yaml_scalar(args.author)}")
    if args.version:
        metadata_lines.append(f"  version: {yaml_scalar(args.version)}")
    for key, value in metadata_items:
        metadata_lines.append(f"  {key}: {yaml_scalar(value)}")

    if metadata_lines:
        lines.append("metadata:")
        lines.extend(metadata_lines)

    lines.extend(
        [
            "---",
            "",
            f"# {args.title or args.name.replace('-', ' ').title()}",
            "",
            "Use this skill when [describe the recurring workflow and the outcome the agent should produce].",
            "",
            "## Workflow",
            "",
            "1. Confirm the user's goal, source files, environment, and constraints.",
            "2. Follow the project- or domain-specific procedure for this workflow.",
            "3. Validate the result before finalizing.",
            "",
            "## Gotchas",
            "",
            "- Replace this with concrete mistakes the agent should avoid.",
            "- Remove generic advice that the agent already knows.",
            "",
            "## Output format",
            "",
            "Use the output format that best fits the user's request. If consistency matters, add a concrete template here.",
        ]
    )
    return "\n".join(lines) + "\n"


def planned_file_status(path: Path, force: bool) -> str:
    if not path.exists():
        return "create"
    if force:
        return "overwrite"
    return "conflict"


def write_file(path: Path, content: str, force: bool) -> None:
    status = planned_file_status(path, force)
    if status == "conflict":
        raise FileExistsError(f"refusing to overwrite existing file without --force: {path}")
    path.write_text(content, encoding="utf-8")


def build_plan(args: argparse.Namespace) -> dict[Path, str]:
    skill_dir = Path(args.skills_root) / args.name
    planned: dict[Path, str] = {
        skill_dir / "SKILL.md": build_skill_md(args),
    }

    if args.with_scripts:
        planned[skill_dir / "scripts" / "README.md"] = "# Scripts\n\nDocument bundled helper scripts here.\n"
    if args.with_references:
        planned[skill_dir / "references" / "README.md"] = "# References\n\nAdd detailed on-demand reference material here.\n"
    if args.with_assets:
        planned[skill_dir / "assets" / "README.md"] = "# Assets\n\nAdd templates, examples, schemas, or static resources here.\n"
    return planned


def print_plan(planned: dict[Path, str], force: bool) -> bool:
    has_conflict = False
    print("Planned files:")
    for path in planned:
        status = planned_file_status(path, force)
        if status == "conflict":
            has_conflict = True
        print(f"- {status}: {path}")
    if has_conflict:
        print("Dry run found existing files that require --force to overwrite.", file=sys.stderr)
    return has_conflict


def validate_args(args: argparse.Namespace) -> None:
    validate_name(args.name)
    if not args.description.strip():
        raise ScaffoldError("description cannot be empty")
    if len(args.description) > 1024:
        raise ScaffoldError("description must be 1024 characters or fewer")
    if args.compatibility and len(args.compatibility) > 500:
        raise ScaffoldError("compatibility must be 500 characters or fewer")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Create a starter Agent Skill directory with compliant frontmatter.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("--skills-root", default="skills", help="Directory containing skill folders")
    parser.add_argument("--name", required=True, help="Skill directory/name, e.g. release-watch")
    parser.add_argument(
        "--description",
        required=True,
        help="Activation-focused description, ideally starting with 'Use this skill when...'",
    )
    parser.add_argument("--title", default="", help="Markdown H1 title; defaults to title-cased name")
    parser.add_argument("--author", default=DEFAULT_AUTHOR, help="Metadata author")
    parser.add_argument("--version", default="0.1.0", help="Optional metadata version")
    parser.add_argument("--license", default="", help="Optional license field, e.g. MIT")
    parser.add_argument("--compatibility", default="", help="Optional compatibility requirements")
    parser.add_argument("--allowed-tools", default="", help="Optional experimental allowed-tools string")
    parser.add_argument(
        "--metadata",
        action="append",
        default=[],
        help="Additional metadata key=value entry; may be repeated",
    )
    parser.add_argument("--with-scripts", action="store_true", help="Create scripts/ with README.md")
    parser.add_argument("--with-references", action="store_true", help="Create references/ with README.md")
    parser.add_argument("--with-assets", action="store_true", help="Create assets/ with README.md")
    parser.add_argument("--force", action="store_true", help="Overwrite existing scaffold files")
    parser.add_argument("--dry-run", action="store_true", help="Print planned files without writing them")
    args = parser.parse_args(argv)

    try:
        validate_args(args)
        planned = build_plan(args)

        if args.dry_run:
            has_conflict = print_plan(planned, args.force)
            return 1 if has_conflict else 0

        for path in planned:
            path.parent.mkdir(parents=True, exist_ok=True)
        for path, content in planned.items():
            write_file(path, content, args.force)

        print(f"Created skill: {Path(args.skills_root) / args.name}")
        for path in planned:
            print(f"- {path}")
        return 0
    except (ScaffoldError, FileExistsError, OSError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
