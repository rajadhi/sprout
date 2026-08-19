#!/usr/bin/env python3
"""
Real, runnable regression test for .github/scripts/check_risk_approval.py -- crafted fixture
trees in a temp directory, real subprocess invocation, real exit codes asserted.
"""
import os
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / ".github" / "scripts" / "check_risk_approval.py"


def run_check(fixture_root):
    env = dict(os.environ, SPROUT_CHECK_ROOT=str(fixture_root))
    result = subprocess.run(
        ["python3", str(SCRIPT)], capture_output=True, text=True, env=env
    )
    return result.returncode, result.stdout


class TestRiskApprovalCheck(unittest.TestCase):
    def test_r3_task_without_approval_ref_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            (tmp / "TASK-900.md").write_text(
                "---\nid: TASK-900\nstatus: READY\nrisk: R3\napproval_ref: null\n---\n\nbody\n"
            )
            code, out = run_check(tmp)
            self.assertEqual(code, 1)
            self.assertIn("approval_ref is not set", out)

    def test_r3_task_with_approval_ref_pointing_nowhere_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            (tmp / "TASK-901.md").write_text(
                "---\nid: TASK-901\nstatus: READY\nrisk: R3\napproval_ref: APR-99999\n---\n\nbody\n"
            )
            code, out = run_check(tmp)
            self.assertEqual(code, 1)
            self.assertIn("no file named APR-99999.md", out)

    def test_r3_task_with_unapproved_record_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            (tmp / "TASK-902.md").write_text(
                "---\nid: TASK-902\nstatus: READY\nrisk: R3\napproval_ref: APR-90002\n---\n\nbody\n"
            )
            (tmp / "APR-90002.md").write_text(
                "---\nid: APR-90002\nartifact: TASK-902\ndecision: rejected\n---\n"
            )
            code, out = run_check(tmp)
            self.assertEqual(code, 1)
            self.assertIn("no decision: approved entry", out)

    def test_r3_task_with_real_approval_passes(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            (tmp / "TASK-903.md").write_text(
                "---\nid: TASK-903\nstatus: READY\nrisk: R3\napproval_ref: APR-90003\n---\n\nbody\n"
            )
            (tmp / "APR-90003.md").write_text(
                "---\nid: APR-90003\nartifact: TASK-903\ndecision: approved\n---\n"
            )
            code, out = run_check(tmp)
            self.assertEqual(code, 0)
            self.assertIn("OK", out)

    def test_r2_task_is_unaffected(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            (tmp / "TASK-904.md").write_text(
                "---\nid: TASK-904\nstatus: READY\nrisk: R2\napproval_ref: null\n---\n\nbody\n"
            )
            code, out = run_check(tmp)
            self.assertEqual(code, 0)

    def test_retired_r3_task_is_exempt(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            (tmp / "TASK-905.md").write_text(
                "---\nid: TASK-905\nstatus: RETIRED\nrisk: R3\napproval_ref: null\n---\n\nbody\n"
            )
            code, out = run_check(tmp)
            self.assertEqual(code, 0)


if __name__ == "__main__":
    unittest.main()
