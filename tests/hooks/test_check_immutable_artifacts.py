#!/usr/bin/env python3
"""
Real, runnable regression test for hooks/check-immutable-artifacts.py -- not a description of
expected behavior, an actual subprocess invocation against real fixture files with assertions on
exit code. Run: python3 tests/hooks/test_check_immutable_artifacts.py
"""
import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HOOK = ROOT / "hooks" / "check-immutable-artifacts.py"


def run_hook(payload):
    result = subprocess.run(
        ["python3", str(HOOK)],
        input=json.dumps(payload),
        capture_output=True,
        text=True,
        cwd=ROOT,
    )
    return result.returncode, result.stderr


class TestImmutabilityHook(unittest.TestCase):
    def test_denies_edit_to_existing_approval_record(self):
        code, stderr = run_hook({
            "tool_name": "Edit",
            "tool_input": {
                "file_path": "docs/examples/ambient-journal/APR-00001.md",
                "old_string": "notes: >",
                "new_string": "notes: changed",
            },
        })
        self.assertEqual(code, 2)
        self.assertIn("immutable record", stderr)

    def test_denies_body_edit_on_superseded_requirement(self):
        code, stderr = run_hook({
            "tool_name": "Edit",
            "tool_input": {
                "file_path": "docs/examples/ambient-journal/REQ-001-v1.md",
                "old_string": "## Problem",
                "new_string": "## Problem (edited)",
            },
        })
        self.assertEqual(code, 2)
        self.assertIn("body content", stderr)

    def test_allows_status_field_transition_on_approved_requirement(self):
        code, _ = run_hook({
            "tool_name": "Edit",
            "tool_input": {
                "file_path": "docs/examples/ambient-journal/REQ-001-v1.md",
                "old_string": "approval_ref: APR-00001",
                "new_string": "approval_ref: APR-00099",
            },
        })
        self.assertEqual(code, 0)

    def test_denies_unallowed_frontmatter_field_change_on_approved_design(self):
        code, stderr = run_hook({
            "tool_name": "Edit",
            "tool_input": {
                "file_path": "docs/examples/ambient-journal/DES-001-v1.md",
                "old_string": 'created_at: "2026-08-19"',
                "new_string": 'created_at: "2099-01-01"',
            },
        })
        self.assertEqual(code, 2)
        self.assertIn("created_at", stderr)

    def test_allows_edit_to_unrestricted_task_file(self):
        code, _ = run_hook({
            "tool_name": "Edit",
            "tool_input": {
                "file_path": "docs/examples/ambient-journal/TASK-003.md",
                "old_string": "status: READY",
                "new_string": "status: CLAIMED",
            },
        })
        self.assertEqual(code, 0)

    def test_allows_write_creating_a_brand_new_versioned_file(self):
        code, _ = run_hook({
            "tool_name": "Write",
            "tool_input": {
                "file_path": "docs/examples/ambient-journal/REQ-999-v1.md",
                "content": "---\nid: REQ-999\n---\nnew\n",
            },
        })
        self.assertEqual(code, 0)


if __name__ == "__main__":
    unittest.main()
