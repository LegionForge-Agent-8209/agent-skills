#!/usr/bin/env python3
"""Create a starter Agent Skill directory.

The generated skill follows the agentskills.io folder convention and writes a
minimal SKILL.md with required frontmatter. The script is intentionally
non-interactive so agents can run it safely from instructions.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

NAME_RE = re.compile(r"^(?!-)(?!.*--)[a-z0-9-]{1,64}(?<!-)$")
DEFAULT_AUTHOR = "LegionForge Agent - Jeli2 directed by jp@legionforge.org"


def validate_name(name: str) -> None:
    if not NAME_RE.match(name):
        raise ValueError(
            "skill name must be 1-64 characters, lowercase letters/numbers/hyphens only, "
            "with no leading, trailing, or consecutive hyphens"
        )


def yaml_quote(value: str) -> str:
    escaped = value.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def build_skill_md(args: argparse.Namespace) -> str:
    lines = ["---", f"name: {args.name}", f"description: {yaml_quote(args.description)}"]

    if args.license:
        lines.append(f"license: {yaml_quote(args.license)}")
    if args.compatibility:
        lines.append(f"compatibility: {yaml_quote(args.compatibility)}")
    if args.allowed_tools:
        lines.append(f"allowed-tools: {yaml_quote(args.allowed_tools)}")

    metadata_lines: list[str] = []
    if args.author:
        metadata_lines.append(f"  author: {yaml_quote(args.author)}")
    if args.version:
        metadata_lines.append(f"  version: {yaml_quote(args.version)}")
    for item in args.metadata:
        if "=" not in item:
            raise ValueError(f"metadata must use key=value format: {item!r}")
        key, value = item.split("=", 1)
        key = key.strip()
        if not key:
            raise ValueError(f"metadata key cannot be empty: {item!r}")
        metadata_lines.append(f"  {key}: {yaml_quote(value.strip())}")

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


def write_file(path: Path, content: str, force: bool) -> None:
    if path.exists() and not force:
        raise FileExistsError(f"refusing to overwrite existing file: {path}")
    path.write_text(content, encoding="utf-8")


def main() -> int:
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
    parser.add_argument("--force", action="store_true", help="Overwrite SKILL.md if it already exists")
    parser.add_argument("--dry-run", action="store_true", help="Print planned files without writing them")
    args = parser.parse_args()

    try:
        validate_name(args.name)
        if not args.description.strip():
            raise ValueError("description cannot be empty")
        if len(args.description) > 1024:
            raise ValueError("description must be 1024 characters or fewer")
        if args.compatibility and len(args.compatibility) > 500:
            raise ValueError("compatibility must be 500 characters or fewer")

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

        if args.dry_run:
            print("Planned files:")
            for path in planned:
                status = "overwrite" if path.exists() else "create"
                print(f"- {status}: {path}")
            return 0

        for path in planned:
            path.parent.mkdir(parents=True, exist_ok=True)
        for path, content in planned.items():
            write_file(path, content, args.force)

        print(f"Created skill: {skill_dir}")
        for path in planned:
            print(f"- {path}")
        return 0
    except (ValueError, FileExistsError, OSError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
