#!/usr/bin/env python3
"""
Real, runnable regression test for .github/scripts/check_merge_readiness.py -- crafted fixture
trees in temp directories, real subprocess invocation, real exit codes asserted. Same pattern as
test_check_risk_approval.py and test_check_skill_scenario_coverage.py.
"""
import os
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / ".github" / "scripts" / "check_merge_readiness.py"

PROJECT_YAML = "verification_policy:\n  mandatory_checks: [lint, unit]\n"


def run_check(root, changed_files="", pr_body="", head_sha="", base_root=None):
    env = dict(
        os.environ,
        SPROUT_CHECK_ROOT=str(root),
        SPROUT_CHANGED_FILES=changed_files,
        SPROUT_PR_BODY=pr_body,
        HEAD_SHA=head_sha,
    )
    if base_root is not None:
        env["SPROUT_BASE_ROOT"] = str(base_root)
    result = subprocess.run(["python3", str(SCRIPT)], capture_output=True, text=True, env=env)
    return result.returncode, result.stdout


def write_task(root, task_id, status, verification_run="null"):
    (root / f"TASK-{task_id}.md").write_text(
        f"---\nid: TASK-{task_id}\nstatus: {status}\n"
        f"verification_run: {verification_run}\n---\n\nbody\n"
    )


def write_run(root, run_id, task_id, commit, verdict, checks, evidence):
    checks_block = "\n".join(f"  - name: {c}\n    result: PASS" for c in checks)
    (root / f"{run_id}.md").write_text(
        f"---\nid: {run_id}\ntask: TASK-{task_id}\ncommit: {commit}\nverdict: {verdict}\n"
        f"evidence: {evidence}\n---\n\nchecks:\n{checks_block}\n"
    )


def write_evidence(root, evd_id, redaction_state):
    (root / f"{evd_id}.md").write_text(
        f"---\nid: {evd_id}\nredaction_state: {redaction_state}\n---\n\nbody\n"
    )


class TestMergeReadinessCheck(unittest.TestCase):
    def test_no_task_reference_passes(self):
        with tempfile.TemporaryDirectory() as tmp:
            code, out = run_check(Path(tmp), changed_files="README.md\n", pr_body="fix a typo")
            self.assertEqual(code, 0)
            self.assertIn("OK", out)

    def test_task_not_verified_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            (tmp / "artifacts").mkdir()
            (tmp / "artifacts" / "project.yaml").write_text(PROJECT_YAML)
            write_task(tmp, "500", status="READY")
            code, out = run_check(tmp, changed_files="TASK-500.md\n", head_sha="abc123")
            self.assertEqual(code, 1)
            self.assertIn("status is READY", out)

    def test_verified_task_without_run_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            write_task(tmp, "501", status="VERIFIED", verification_run="null")
            code, out = run_check(tmp, changed_files="TASK-501.md\n", head_sha="abc123")
            self.assertEqual(code, 1)
            self.assertIn("verification_run is not set", out)

    def test_run_wrong_commit_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            (tmp / "artifacts").mkdir()
            (tmp / "artifacts" / "project.yaml").write_text(PROJECT_YAML)
            write_task(tmp, "502", status="VERIFIED", verification_run="RUN-00502")
            write_run(tmp, "RUN-00502", "502", commit="a1b2c3d", verdict="PASS",
                      checks=["lint", "unit"], evidence="[EVD-00502]")
            write_evidence(tmp, "EVD-00502", "redacted")
            code, out = run_check(tmp, changed_files="TASK-502.md\n", head_sha="f9e8d7c")
            self.assertEqual(code, 1)
            self.assertIn("neither the PR head", out)

    def test_run_missing_mandatory_check_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            (tmp / "artifacts").mkdir()
            (tmp / "artifacts" / "project.yaml").write_text(PROJECT_YAML)
            write_task(tmp, "503", status="VERIFIED", verification_run="RUN-00503")
            write_run(tmp, "RUN-00503", "503", commit="deadbeef", verdict="PASS",
                      checks=["unit"], evidence="[EVD-00503]")
            write_evidence(tmp, "EVD-00503", "redacted")
            code, out = run_check(tmp, changed_files="TASK-503.md\n", head_sha="deadbeef")
            self.assertEqual(code, 1)
            self.assertIn("'lint'", out)

    def test_unredacted_evidence_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            (tmp / "artifacts").mkdir()
            (tmp / "artifacts" / "project.yaml").write_text(PROJECT_YAML)
            write_task(tmp, "504", status="VERIFIED", verification_run="RUN-00504")
            write_run(tmp, "RUN-00504", "504", commit="deadbeef", verdict="PASS",
                      checks=["lint", "unit"], evidence="[EVD-00504]")
            write_evidence(tmp, "EVD-00504", "unredacted")
            code, out = run_check(tmp, changed_files="TASK-504.md\n", head_sha="deadbeef")
            self.assertEqual(code, 1)
            self.assertIn("not safe to merge on", out)

    def test_fully_valid_binding_passes(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            (tmp / "artifacts").mkdir()
            (tmp / "artifacts" / "project.yaml").write_text(PROJECT_YAML)
            write_task(tmp, "505", status="VERIFIED", verification_run="RUN-00505")
            write_run(tmp, "RUN-00505", "505", commit="deadbeef", verdict="PASS",
                      checks=["lint", "unit"], evidence="[EVD-00505]")
            write_evidence(tmp, "EVD-00505", "redacted")
            code, out = run_check(tmp, changed_files="TASK-505.md\n", head_sha="deadbeef")
            self.assertEqual(code, 0)
            self.assertIn("OK", out)

    def test_task_reference_from_pr_body_only(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            (tmp / "artifacts").mkdir()
            (tmp / "artifacts" / "project.yaml").write_text(PROJECT_YAML)
            write_task(tmp, "506", status="READY")
            code, out = run_check(
                tmp, changed_files="src/thing.py\n", pr_body="Task: TASK-506", head_sha="x"
            )
            self.assertEqual(code, 1)
            self.assertIn("status is READY", out)

    def test_backward_status_transition_fails(self):
        with tempfile.TemporaryDirectory() as tmp, tempfile.TemporaryDirectory() as base:
            tmp, base = Path(tmp), Path(base)
            (base / "REQ-007.md").write_text(
                "---\nid: REQ-007\nstatus: APPROVED\n---\n\noriginal body\n"
            )
            (tmp / "REQ-007.md").write_text(
                "---\nid: REQ-007\nstatus: PROPOSED\n---\n\nrewritten body\n"
            )
            code, out = run_check(tmp, changed_files="REQ-007.md\n", base_root=base)
            self.assertEqual(code, 1)
            self.assertIn("illegal transition APPROVED -> PROPOSED", out)

    def test_body_change_alongside_legal_transition_fails(self):
        with tempfile.TemporaryDirectory() as tmp, tempfile.TemporaryDirectory() as base:
            tmp, base = Path(tmp), Path(base)
            (base / "REQ-008.md").write_text(
                "---\nid: REQ-008\nstatus: APPROVED\n---\n\noriginal body\n"
            )
            (tmp / "REQ-008.md").write_text(
                "---\nid: REQ-008\nstatus: SUPERSEDED\nsuperseded_by: REQ-009\n---\n\nedited body\n"
            )
            code, out = run_check(tmp, changed_files="REQ-008.md\n", base_root=base)
            self.assertEqual(code, 1)
            self.assertIn("body changed", out)

    def test_legal_transition_no_body_change_passes(self):
        with tempfile.TemporaryDirectory() as tmp, tempfile.TemporaryDirectory() as base:
            tmp, base = Path(tmp), Path(base)
            (base / "REQ-010.md").write_text(
                "---\nid: REQ-010\nstatus: APPROVED\n---\n\nsame body\n"
            )
            (tmp / "REQ-010.md").write_text(
                "---\nid: REQ-010\nstatus: SUPERSEDED\nsuperseded_by: REQ-011\n---\n\nsame body\n"
            )
            code, out = run_check(tmp, changed_files="REQ-010.md\n", base_root=base)
            self.assertEqual(code, 0)

    def test_new_locked_prefix_file_is_not_flagged(self):
        with tempfile.TemporaryDirectory() as tmp, tempfile.TemporaryDirectory() as base:
            tmp, base = Path(tmp), Path(base)
            (tmp / "REQ-020.md").write_text("---\nid: REQ-020\nstatus: PROPOSED\n---\n\nnew\n")
            code, out = run_check(tmp, changed_files="REQ-020.md\n", base_root=base)
            self.assertEqual(code, 0)

    def test_no_base_sha_skips(self):
        with tempfile.TemporaryDirectory() as tmp:
            env = dict(os.environ, SPROUT_CHECK_ROOT=str(tmp))
            env.pop("SPROUT_CHANGED_FILES", None)
            env["BASE_SHA"] = "0000000000000000000000000000000000000000"
            result = subprocess.run(["python3", str(SCRIPT)], capture_output=True, text=True, env=env)
            self.assertEqual(result.returncode, 0)
            self.assertIn("skipping", result.stdout)


if __name__ == "__main__":
    unittest.main()
