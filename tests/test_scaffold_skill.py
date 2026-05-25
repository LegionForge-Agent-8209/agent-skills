from __future__ import annotations

import importlib.util
import subprocess
import sys
import tempfile
import unittest
from argparse import Namespace
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = REPO_ROOT / "skills" / "agent-skill-authoring" / "scripts" / "scaffold_skill.py"

spec = importlib.util.spec_from_file_location("scaffold_skill", SCRIPT_PATH)
scaffold_skill = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(scaffold_skill)


class ScaffoldSkillTests(unittest.TestCase):
    def make_args(self, **overrides: object) -> Namespace:
        values = {
            "skills_root": "skills",
            "name": "example-skill",
            "description": "Use this skill when testing special characters: quotes, tabs\t, and newlines\nwork.",
            "title": "",
            "author": scaffold_skill.DEFAULT_AUTHOR,
            "version": "0.1.0",
            "license": "MIT",
            "compatibility": "Requires Python 3.9+ and paths like C:\\tmp\\skills.",
            "allowed_tools": "Read Bash(git:*)",
            "metadata": ["source=unit-test", "notes=value: with colon"],
            "with_scripts": False,
            "with_references": False,
            "with_assets": False,
            "force": False,
            "dry_run": False,
        }
        values.update(overrides)
        return Namespace(**values)

    def test_build_skill_md_escapes_yaml_scalars(self) -> None:
        text = scaffold_skill.build_skill_md(self.make_args())

        self.assertIn('description: "Use this skill when testing special characters:', text)
        self.assertIn('newlines\\nwork."', text)
        self.assertIn('compatibility: "Requires Python 3.9+ and paths like C:\\\\tmp\\\\skills."', text)
        self.assertIn('author: "LegionForge Agent - Jeli2 directed by jp@legionforge.org"', text)
        self.assertIn('notes: "value: with colon"', text)

    def test_dry_run_reports_conflict_without_force(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            existing = Path(tmp) / "example-skill" / "SKILL.md"
            existing.parent.mkdir(parents=True)
            existing.write_text("existing", encoding="utf-8")

            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT_PATH),
                    "--skills-root",
                    tmp,
                    "--name",
                    "example-skill",
                    "--description",
                    "Use this skill when testing dry-run conflicts.",
                    "--dry-run",
                ],
                check=False,
                capture_output=True,
                text=True,
            )

        self.assertEqual(result.returncode, 1)
        self.assertIn("conflict:", result.stdout)
        self.assertIn("require --force", result.stderr)

    def test_dry_run_reports_overwrite_with_force(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            existing = Path(tmp) / "example-skill" / "SKILL.md"
            existing.parent.mkdir(parents=True)
            existing.write_text("existing", encoding="utf-8")

            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT_PATH),
                    "--skills-root",
                    tmp,
                    "--name",
                    "example-skill",
                    "--description",
                    "Use this skill when testing forced dry-run overwrites.",
                    "--dry-run",
                    "--force",
                ],
                check=False,
                capture_output=True,
                text=True,
            )

        self.assertEqual(result.returncode, 0)
        self.assertIn("overwrite:", result.stdout)
        self.assertEqual(result.stderr, "")

    def test_create_refuses_existing_file_without_force(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            existing = Path(tmp) / "example-skill" / "SKILL.md"
            existing.parent.mkdir(parents=True)
            existing.write_text("existing", encoding="utf-8")

            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT_PATH),
                    "--skills-root",
                    tmp,
                    "--name",
                    "example-skill",
                    "--description",
                    "Use this skill when testing create conflicts.",
                ],
                check=False,
                capture_output=True,
                text=True,
            )

            self.assertEqual(existing.read_text(encoding="utf-8"), "existing")

        self.assertEqual(result.returncode, 1)
        self.assertIn("without --force", result.stderr)

    def test_create_can_force_overwrite_existing_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            existing = Path(tmp) / "example-skill" / "SKILL.md"
            existing.parent.mkdir(parents=True)
            existing.write_text("existing", encoding="utf-8")

            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT_PATH),
                    "--skills-root",
                    tmp,
                    "--name",
                    "example-skill",
                    "--description",
                    "Use this skill when testing forced overwrites.",
                    "--force",
                ],
                check=False,
                capture_output=True,
                text=True,
            )

            content = existing.read_text(encoding="utf-8")

        self.assertEqual(result.returncode, 0)
        self.assertIn("Created skill:", result.stdout)
        self.assertIn("description: \"Use this skill when testing forced overwrites.\"", content)


if __name__ == "__main__":
    unittest.main()
