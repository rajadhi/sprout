#!/usr/bin/env python3
"""
Deterministic CI check: every R3/R4 task must have a real, approved approval record.

Why this exists: docs/protocol.md §40's autonomy policy says R3/R4 work needs human approval,
but on a solo-maintainer repo `required_pull_request_reviews.required_approving_review_count`
can't meaningfully enforce that (see docs/examples/github-dogfood.md -- enforce_admins: false is
a deliberate gap). This check gives R3/R4 approval real teeth as a required status check instead:
it doesn't matter whether a human reviewer exists, the task file itself must carry a real
approval_ref pointing at an APR-*.md record that says decision: approved and names this task.

Scans every *.md file in the repo whose frontmatter has `id: TASK-*` -- not diff-based, a
whole-repo invariant, same style as validate_structure.py.
"""
import os
import re
import sys
from pathlib import Path

ROOT = Path(os.environ.get("SPROUT_CHECK_ROOT") or Path(__file__).resolve().parents[2])
FRONTMATTER_RE = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)
HIGH_RISK = {"R3", "R4"}

errors = []


def parse_field(frontmatter, key):
    m = re.search(rf"^{key}:\s*(.*)$", frontmatter, re.MULTILINE)
    return m.group(1).strip() if m else None


def find_task_files():
    for path in ROOT.rglob("*.md"):
        if ".git" in path.parts:
            continue
        text = path.read_text(errors="ignore")
        m = FRONTMATTER_RE.match(text)
        if not m:
            continue
        if re.match(r"^id:\s*TASK-", m.group(1), re.MULTILINE):
            yield path, m.group(1)


def find_approval(approval_ref, task_id):
    """Return True if approval_ref resolves to a real APR-*.md with decision: approved
    that names this task id."""
    candidates = list(ROOT.rglob(f"{approval_ref}.md"))
    if not candidates:
        return False, f"no file named {approval_ref}.md found anywhere in the repo"
    for apr_path in candidates:
        text = apr_path.read_text(errors="ignore")
        m = FRONTMATTER_RE.match(text)
        if not m:
            continue
        fm = m.group(1)
        decision = (parse_field(fm, "decision") or "").lower()
        artifact_field = parse_field(fm, "artifact") or ""
        if decision == "approved" and task_id in artifact_field:
            return True, None
    return False, f"{approval_ref}.md exists but has no decision: approved entry naming {task_id}"


def main():
    for path, frontmatter in find_task_files():
        risk = (parse_field(frontmatter, "risk") or "").strip()
        if risk not in HIGH_RISK:
            continue

        task_id = parse_field(frontmatter, "id")
        status = (parse_field(frontmatter, "status") or "").strip()
        if status == "RETIRED":
            continue  # a retired R3/R4 task was never implemented; nothing to approve

        approval_ref = parse_field(frontmatter, "approval_ref")
        if not approval_ref or approval_ref.strip().lower() == "null":
            errors.append(
                f"{path}: risk {risk} but approval_ref is not set. "
                f"docs/protocol.md §40 requires human approval for R3/R4 -- "
                f"set approval_ref to a real APR-*.md that approves {task_id}."
            )
            continue

        ok, reason = find_approval(approval_ref.strip(), task_id)
        if not ok:
            errors.append(f"{path}: risk {risk}, approval_ref {approval_ref} -- {reason}.")

    if errors:
        print(f"R3/R4 approval check failed ({len(errors)} issue(s)):")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)

    print("OK: every R3/R4 task has a real, approved approval record.")


if __name__ == "__main__":
    main()
