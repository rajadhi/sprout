#!/usr/bin/env python3
"""
Real, runnable regression test for .github/scripts/check_plugin_version_bump.py -- same pattern
as test_check_skill_scenario_coverage.py (SPROUT_CHANGED_FILES override) plus
SPROUT_OLD_VERSION/SPROUT_NEW_VERSION overrides for the version-comparison side.
"""
import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / ".github" / "scripts" / "check_plugin_version_bump.py"


def run_check(changed_files_text, old_version=None, new_version="0.3.0", root=None):
    env = dict(os.environ, SPROUT_CHANGED_FILES=changed_files_text, SPROUT_NEW_VERSION=new_version)
    if old_version is not None:
        env["SPROUT_OLD_VERSION"] = old_version
    else:
        env.pop("SPROUT_OLD_VERSION", None)
    if root is not None:
        env["SPROUT_CHECK_ROOT"] = str(root)
    result = subprocess.run(["python3", str(SCRIPT)], capture_output=True, text=True, env=env)
    return result.returncode, result.stdout


class TestPluginVersionBumpCheck(unittest.TestCase):
    def test_no_significant_paths_passes_without_version_check(self):
        code, out = run_check("README.md\ndocs/protocol.md\n")
        self.assertEqual(code, 0)
        self.assertIn("no significant plugin paths changed", out)

    def test_significant_path_without_version_bump_fails(self):
        code, out = run_check(
            "skills/upgrade/SKILL.md\n", old_version="0.3.0", new_version="0.3.0"
        )
        self.assertEqual(code, 1)
        self.assertIn("did not increase", out)

    def test_significant_path_with_patch_bump_passes(self):
        code, out = run_check(
            "skills/upgrade/SKILL.md\n", old_version="0.3.0", new_version="0.3.1"
        )
        self.assertEqual(code, 0)
        self.assertIn("OK", out)

    def test_significant_path_with_minor_bump_passes(self):
        code, out = run_check(
            ".github/scripts/check_merge_readiness.py\n", old_version="0.3.0", new_version="0.4.0"
        )
        self.assertEqual(code, 0)

    def test_significant_path_with_major_bump_passes(self):
        code, out = run_check(
            "hooks/check-immutable-artifacts.py\n", old_version="0.3.0", new_version="1.0.0"
        )
        self.assertEqual(code, 0)

    def test_version_decrease_fails(self):
        code, out = run_check(
            "agents/verifier.md\n", old_version="0.3.0", new_version="0.2.9"
        )
        self.assertEqual(code, 1)
        self.assertIn("did not increase", out)

    def test_docs_and_tests_only_change_does_not_require_bump(self):
        code, out = run_check("docs/examples/schema-migration/MIGRATION.md\ntests/ci/test_foo.py\n")
        self.assertEqual(code, 0)
        self.assertIn("no significant plugin paths changed", out)

    def test_codeowners_change_counts_as_significant(self):
        code, out = run_check("CODEOWNERS\n", old_version="0.3.0", new_version="0.3.0")
        self.assertEqual(code, 1)

    def test_no_base_sha_skips(self):
        env = dict(os.environ)
        env.pop("SPROUT_CHANGED_FILES", None)
        env["BASE_SHA"] = "0000000000000000000000000000000000000000"
        result = subprocess.run(["python3", str(SCRIPT)], capture_output=True, text=True, env=env)
        self.assertEqual(result.returncode, 0)
        self.assertIn("skipping", result.stdout)

    def test_real_plugin_json_is_readable(self):
        # Sanity check against the actual repo file (no overrides) -- confirms parse_version
        # works against the real .claude-plugin/plugin.json shape, not just synthetic overrides.
        real = json.loads((ROOT / ".claude-plugin" / "plugin.json").read_text())
        self.assertRegex(real["version"], r"^\d+\.\d+\.\d+$")


if __name__ == "__main__":
    unittest.main()
