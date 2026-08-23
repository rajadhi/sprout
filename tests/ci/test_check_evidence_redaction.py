#!/usr/bin/env python3
"""
Real, runnable regression test for .github/scripts/check_evidence_redaction.py -- crafted
fixture trees in a temp directory, real subprocess invocation, real exit codes asserted.
"""
import os
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / ".github" / "scripts" / "check_evidence_redaction.py"


def run_check(fixture_root):
    env = dict(os.environ, SPROUT_CHECK_ROOT=str(fixture_root))
    result = subprocess.run(
        ["python3", str(SCRIPT)], capture_output=True, text=True, env=env
    )
    return result.returncode, result.stdout


class TestEvidenceRedactionCheck(unittest.TestCase):
    def test_unredacted_evidence_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            (tmp / "EVD-900.md").write_text(
                "---\nid: EVD-900\ntype: LOG\nredaction_state: unredacted\n---\n\nclean body\n"
            )
            code, out = run_check(tmp)
            self.assertEqual(code, 1)
            self.assertIn("redaction_state is 'unredacted'", out)

    def test_not_applicable_clean_content_passes(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            (tmp / "EVD-901.md").write_text(
                "---\nid: EVD-901\ntype: UNIT_TEST_RESULT\nredaction_state: not_applicable\n"
                "---\n\nAll 5 tests passed.\n"
            )
            code, out = run_check(tmp)
            self.assertEqual(code, 0)
            self.assertIn("OK", out)

    def test_redacted_state_with_bearer_token_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            (tmp / "EVD-902.md").write_text(
                "---\nid: EVD-902\ntype: API_RESPONSE\nredaction_state: redacted\n---\n\n"
                "Authorization: Bearer abcdefghijklmnopqrstuvwxyz012345\n"
            )
            code, out = run_check(tmp)
            self.assertEqual(code, 1)
            self.assertIn("bearer token", out)

    def test_redacted_state_with_password_assignment_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            (tmp / "EVD-903.md").write_text(
                '---\nid: EVD-903\ntype: LOG\nredaction_state: redacted\n---\n\n'
                'password: "hunter2222"\n'
            )
            code, out = run_check(tmp)
            self.assertEqual(code, 1)
            self.assertIn("password assignment", out)

    def test_template_placeholder_is_exempt(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            (tmp / "evidence.md").write_text(
                "---\nid: EVD-XXXXXX\ntype: unknown\nredaction_state: unredacted\n---\n\n"
                "## Content\n"
            )
            code, out = run_check(tmp)
            self.assertEqual(code, 0)

    def test_non_evidence_file_is_ignored(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            (tmp / "TASK-900.md").write_text(
                "---\nid: TASK-900\nstatus: READY\n---\n\npassword: \"hunter2222\"\n"
            )
            code, out = run_check(tmp)
            self.assertEqual(code, 0)


if __name__ == "__main__":
    unittest.main()
