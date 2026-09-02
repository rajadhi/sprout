#!/usr/bin/env python3
"""
Deterministic CI check: a PR claiming a task must bind to a real VERIFIED task, a matching PASS
verification run captured against this exact commit, mandatory-check coverage, valid evidence,
and no illegal backward status transition on a locked artifact in the diff.

Why this exists: an external review of an earlier version of this repo correctly flagged that
merge_policy (artifacts/project.yaml) was declarative only -- nothing checked a PR's claimed task
against a real VERIFIED status, a matching PASS run bound to the PR's exact head commit, mandatory
checks satisfied, or valid evidence. A code-only PR could pass CI without participating in
Sprout's own policy at all. An earlier attempt at this check ran as a headless Claude Code
invocation (see git history for skills/merge-readiness/SKILL.md) -- replaced with this script
because the relational logic here (task -> run -> evidence -> commit SHA, plus a fixed
forward-only transition table) is fully expressible deterministically, and a deterministic check
needs no API key/OAuth token, no network call, and no per-PR judgment call on exactly the
invariant this repo cares most about proving mechanically. Same reasoning CLAUDE.md's own
preference order gives for "tiny deterministic helper" over reaching for an agent.

Portable to any downstream repo regardless of tech stack: unlike lint/build/test steps (which
need the project's own toolchain), this check only ever reads Sprout's own schema-defined
artifact files, so init can hand it to any project as-is (skills/init/SKILL.md step 9).

The status-transition portion intentionally duplicates a small amount of logic from
hooks/check-immutable-artifacts.py rather than importing it -- that hook operates on a live
Edit/Write tool call (old_string/new_string), this operates on a diff between two commits; same
invariant (docs/protocol.md §1.5), two different entry points, see docs/architecture.md §5's note
that the hook is a local guardrail and this script is the actual CI-facing enforcement boundary.

Inputs (env vars, mirroring the pattern check_skill_scenario_coverage.py already uses):
  SPROUT_CHECK_ROOT     -- root to scan for current (HEAD) artifact files. Defaults to the repo.
  SPROUT_CHANGED_FILES  -- newline-separated changed paths, overrides git diff (tests/manual runs).
  BASE_SHA / HEAD_SHA   -- commit range for `git diff` when SPROUT_CHANGED_FILES isn't set.
  SPROUT_PR_BODY        -- the PR description text, for a bare "Task: TASK-XXX" reference when no
                           task file itself is in the diff.
  SPROUT_BASE_ROOT      -- root holding base-commit content of changed files, overrides `git show
                           BASE_SHA:path` (tests/manual runs).
"""
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(os.environ.get("SPROUT_CHECK_ROOT") or Path(__file__).resolve().parents[2])
FRONTMATTER_RE = re.compile(r"\A---\n(.*?)\n---\n(.*)\Z", re.DOTALL)
TASK_ID_RE = re.compile(r"TASK-\d+")

LOCKED_PREFIXES = ("REQ-", "DES-", "ADR-", "DEC-")
# Paths under these prefixes are documentation/fixture content (docs/examples/ambient-journal,
# docs/examples/schema-migration, tests/fixtures/toy-app, ...) -- TASK-*.md files there describe
# or demonstrate the schema, they aren't real tasks this repo is claiming to have verified. A
# TASK-*.md matched here would otherwise make every PR that touches an example directory fail on
# "status is MERGED, not VERIFIED" for a task that was never meant to bind to anything.
EXAMPLE_DIR_PREFIXES = ("docs/examples/", "tests/fixtures/")
LOCKED_STATUSES = {"APPROVED", "SUPERSEDED", "VERIFIED", "ACCEPTED"}
LEGAL_FORWARD = {
    "APPROVED": {"SUPERSEDED", "VERIFIED"},
    "ACCEPTED": {"SUPERSEDED"},
    "SUPERSEDED": set(),
    "VERIFIED": set(),
}
ALLOWED_LOCKED_FIELDS = {"status", "supersedes", "superseded_by", "approved_at", "approval_ref"}

errors = []


def parse_field(frontmatter, key):
    m = re.search(rf"^{key}:\s*(.*)$", frontmatter, re.MULTILINE)
    return m.group(1).strip() if m else None


def split_frontmatter(text):
    m = FRONTMATTER_RE.match(text)
    if not m:
        return None, None
    return m.group(1), m.group(2)


def changed_field_names(old_fm, new_fm):
    old_lines = set(old_fm.splitlines())
    new_lines = set(new_fm.splitlines())
    fields = set()
    for line in old_lines.symmetric_difference(new_lines):
        m = re.match(r"^([A-Za-z_][A-Za-z0-9_]*):", line)
        fields.add(m.group(1) if m else "<unparseable-line>")
    return fields


def changed_files():
    override = os.environ.get("SPROUT_CHANGED_FILES")
    if override is not None:
        return [line.strip() for line in override.splitlines() if line.strip()]

    base_sha = os.environ.get("BASE_SHA")
    head_sha = os.environ.get("HEAD_SHA", "HEAD")
    if not base_sha or set(base_sha) == {"0"}:
        return None

    result = subprocess.run(
        ["git", "diff", "--name-only", base_sha, head_sha], capture_output=True, text=True, cwd=ROOT
    )
    if result.returncode != 0:
        return None
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


def base_content(path):
    """Pre-PR (base commit) content of a changed file, or None if it didn't exist yet."""
    base_root = os.environ.get("SPROUT_BASE_ROOT")
    if base_root is not None:
        candidate = Path(base_root) / path
        return candidate.read_text() if candidate.exists() else None

    base_sha = os.environ.get("BASE_SHA")
    if not base_sha or set(base_sha) == {"0"}:
        return None
    result = subprocess.run(
        ["git", "show", f"{base_sha}:{path}"], capture_output=True, text=True, cwd=ROOT
    )
    return result.stdout if result.returncode == 0 else None


def find_artifact(prefix_id):
    candidates = [
        p for p in ROOT.rglob(f"{prefix_id}.md")
        if not any(p.relative_to(ROOT).as_posix().startswith(pre) for pre in EXAMPLE_DIR_PREFIXES)
    ]
    return candidates[0] if candidates else None


def mandatory_checks():
    profile = ROOT / ".sprout" / "project.yaml"
    if not profile.exists():
        profile = ROOT / "artifacts" / "project.yaml"
    if not profile.exists():
        return []
    text = profile.read_text()
    m = re.search(r"mandatory_checks:\s*\[([^\]]*)\]", text)
    if not m:
        return []
    return [c.strip() for c in m.group(1).split(",") if c.strip()]


def check_names_from_run(run_frontmatter, run_body):
    # `checks:` is a YAML list of {name, result} mappings in the body, not the frontmatter --
    # see artifacts/verification-run.md. Pull every "name: X" that follows a "checks:" line.
    m = re.search(r"^checks:\s*$(.*?)(?:\n\S|\Z)", run_body, re.MULTILINE | re.DOTALL)
    block = m.group(1) if m else ""
    return set(re.findall(r"name:\s*(\S+)", block))


def check_task_binding(task_id, head_sha):
    task_path = find_artifact(f"TASK-{task_id}")
    if not task_path:
        errors.append(f"TASK-{task_id}: referenced by this PR but no such task file exists.")
        return
    fm, _ = split_frontmatter(task_path.read_text())
    if fm is None:
        errors.append(f"{task_path}: no parseable frontmatter, can't confirm VERIFIED status.")
        return

    status = (parse_field(fm, "status") or "").strip()
    if status != "VERIFIED":
        errors.append(f"{task_path}: status is {status or '(unset)'}, not VERIFIED.")
        return

    run_id = (parse_field(fm, "verification_run") or "").strip()
    if not run_id or run_id.lower() == "null":
        errors.append(f"{task_path}: status VERIFIED but verification_run is not set.")
        return

    run_path = find_artifact(run_id)
    if not run_path:
        errors.append(f"{task_path}: verification_run {run_id} points at a file that doesn't exist.")
        return

    run_fm, run_body = split_frontmatter(run_path.read_text())
    if run_fm is None:
        errors.append(f"{run_path}: no parseable frontmatter.")
        return

    verdict = (parse_field(run_fm, "verdict") or "").strip()
    if verdict != "PASS":
        errors.append(f"{run_path}: verdict is {verdict or '(unset)'}, not PASS.")

    commit = (parse_field(run_fm, "commit") or "").strip()
    if head_sha and commit != head_sha:
        is_ancestor = subprocess.run(
            ["git", "merge-base", "--is-ancestor", commit, head_sha], cwd=ROOT
        ).returncode == 0 if commit and os.environ.get("SPROUT_BASE_ROOT") is None else False
        if not is_ancestor:
            errors.append(
                f"{run_path}: commit {commit!r} is neither the PR head ({head_sha}) nor an "
                f"ancestor of it -- this run doesn't prove the current diff was verified."
            )

    required = set(mandatory_checks())
    covered = check_names_from_run(run_fm, run_body)
    missing = required - covered
    if missing:
        errors.append(
            f"{run_path}: verdict PASS but never covered mandatory check(s) "
            f"{sorted(missing)} (project.yaml verification_policy.mandatory_checks)."
        )

    evidence_ids = re.findall(r"EVD-\S+", (parse_field(run_fm, "evidence") or ""))
    if covered and not evidence_ids:
        errors.append(f"{run_path}: has checks but no evidence records referenced.")
    for evd_id in evidence_ids:
        evd_path = find_artifact(evd_id.rstrip(",]"))
        if not evd_path:
            errors.append(f"{run_path}: references {evd_id} but no such evidence file exists.")
            continue
        evd_fm, _ = split_frontmatter(evd_path.read_text())
        redaction = (parse_field(evd_fm, "redaction_state") or "").strip() if evd_fm else ""
        if redaction not in ("redacted", "not_applicable"):
            errors.append(f"{evd_path}: redaction_state is {redaction or '(unset)'}, not safe to merge on.")


def check_transitions(files):
    for f in files:
        if not any(Path(f).name.startswith(p) for p in LOCKED_PREFIXES):
            continue
        old_text = base_content(f)
        if old_text is None:
            continue  # new file in this PR -- nothing to have locked yet

        old_fm, old_body = split_frontmatter(old_text)
        if old_fm is None:
            continue
        old_status = (parse_field(old_fm, "status") or "").upper()
        if old_status not in LOCKED_STATUSES:
            continue

        new_path = ROOT / f
        if not new_path.exists():
            errors.append(f"{f}: deleted, but was {old_status} on the base branch -- immutable records aren't removable.")
            continue
        new_fm, new_body = split_frontmatter(new_path.read_text())
        if new_fm is None:
            errors.append(f"{f}: base status was {old_status} but this PR strips its frontmatter entirely.")
            continue

        new_status = (parse_field(new_fm, "status") or "").upper()
        if new_status != old_status:
            if new_status not in LEGAL_FORWARD.get(old_status, set()):
                errors.append(f"{f}: illegal transition {old_status} -> {new_status or '(unset)'}.")
                continue

        if new_body != old_body:
            errors.append(f"{f}: body changed while base status was {old_status} -- immutable once locked (docs/protocol.md §1.5).")
            continue

        offending = changed_field_names(old_fm, new_fm) - ALLOWED_LOCKED_FIELDS
        if offending:
            errors.append(f"{f}: changed frontmatter field(s) {sorted(offending)} on a {old_status} artifact -- only {sorted(ALLOWED_LOCKED_FIELDS)} may change.")


def main():
    files = changed_files()
    if files is None:
        print("OK: no base to diff against (new branch or missing BASE_SHA) -- skipping.")
        return

    pr_body = os.environ.get("SPROUT_PR_BODY", "")
    head_sha = os.environ.get("HEAD_SHA")

    task_ids = set()
    for f in files:
        if any(f.startswith(pre) for pre in EXAMPLE_DIR_PREFIXES):
            continue
        m = re.match(r"^(?:.*/)?TASK-(\d+)\.md$", f)
        if m:
            task_ids.add(m.group(1))
    for m in TASK_ID_RE.finditer(pr_body):
        task_ids.add(m.group(0).split("-", 1)[1])

    if task_ids:
        for task_id in sorted(task_ids):
            check_task_binding(task_id, head_sha)
    # No task reference anywhere (diff or PR body): nothing to bind, deliberately not an error --
    # blocking every PR that doesn't touch Sprout artifacts would be scope creep past merge_policy.

    check_transitions(files)

    if errors:
        print(f"Merge readiness check failed ({len(errors)} issue(s)):")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)

    print("OK: merge readiness checks passed.")


if __name__ == "__main__":
    main()
