#!/usr/bin/env python3
"""
Real, runnable regression test for .github/scripts/check_skill_scenario_coverage.py -- injects a
changed-file list via SPROUT_CHANGED_FILES (the same override the script supports for tests and
manual runs), real subprocess invocation, real exit codes asserted.
"""
import os
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / ".github" / "scripts" / "check_skill_scenario_coverage.py"


def run_check(changed_files_text):
    env = dict(os.environ, SPROUT_CHANGED_FILES=changed_files_text)
    result = subprocess.run(
        ["python3", str(SCRIPT)], capture_output=True, text=True, env=env
    )
    return result.returncode, result.stdout


class TestSkillScenarioCoverageCheck(unittest.TestCase):
    def test_skill_change_without_scenario_fails(self):
        code, out = run_check("skills/plan/SKILL.md\n")
        self.assertEqual(code, 1)
        self.assertIn("skills/plan/SKILL.md changed", out)

    def test_skill_change_with_scenario_passes(self):
        code, out = run_check("skills/shape/SKILL.md\ntests/scenarios/shape/new-case.md\n")
        self.assertEqual(code, 0)
        self.assertIn("OK", out)

    def test_no_skill_files_changed_passes(self):
        code, out = run_check("README.md\ndocs/protocol.md\n")
        self.assertEqual(code, 0)

    def test_multiple_skills_one_missing_scenario(self):
        code, out = run_check(
            "skills/shape/SKILL.md\ntests/scenarios/shape/x.md\nskills/plan/SKILL.md\n"
        )
        self.assertEqual(code, 1)
        self.assertIn("skills/plan/SKILL.md changed", out)
        self.assertNotIn("skills/shape/SKILL.md changed", out)

    def test_no_changed_files_passes(self):
        code, out = run_check("")
        self.assertEqual(code, 0)

    def test_scenario_in_different_skill_dir_does_not_count(self):
        code, out = run_check("skills/plan/SKILL.md\ntests/scenarios/shape/x.md\n")
        self.assertEqual(code, 1)
        self.assertIn("skills/plan/SKILL.md changed", out)


if __name__ == "__main__":
    unittest.main()
