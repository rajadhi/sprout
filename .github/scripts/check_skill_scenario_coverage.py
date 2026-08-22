#!/usr/bin/env python3
"""
Deterministic CI check: a change that edits skills/<name>/SKILL.md must also touch at least one
file under tests/scenarios/<name>/ in the same change.

Why this exists: CLAUDE.md's "Framework governance" section says a skill change needs a pressure
scenario in tests/scenarios/ demonstrating the skill resists the failure it's meant to prevent --
a discipline rule that had no enforcement. This doesn't judge whether the scenario is any good
(that needs human/agent judgment, out of scope for a deterministic check per
docs/architecture.md §5's "hooks are for enforcement that doesn't need LLM judgment") -- it only
checks that a scenario file was touched at all.

Changed files come from `git diff --name-only BASE_SHA HEAD_SHA`, using BASE_SHA/HEAD_SHA set by
the workflow (see .github/workflows/ci.yml), or from SPROUT_CHANGED_FILES (newline-separated
paths) as a direct override for tests and manual runs.
"""
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(os.environ.get("SPROUT_CHECK_ROOT") or Path(__file__).resolve().parents[2])
SKILL_RE = re.compile(r"^skills/([^/]+)/SKILL\.md$")
SCENARIO_RE = re.compile(r"^tests/scenarios/([^/]+)/")


def changed_files():
    override = os.environ.get("SPROUT_CHANGED_FILES")
    if override is not None:
        return [line.strip() for line in override.splitlines() if line.strip()]

    base_sha = os.environ.get("BASE_SHA")
    head_sha = os.environ.get("HEAD_SHA", "HEAD")
    if not base_sha or set(base_sha) == {"0"}:
        return None  # nothing to diff against (new branch, or not running in a workflow)

    result = subprocess.run(
        ["git", "diff", "--name-only", base_sha, head_sha],
        capture_output=True, text=True, cwd=ROOT,
    )
    if result.returncode != 0:
        return None
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


def main():
    files = changed_files()
    if files is None:
        print("OK: no base to diff against (new branch or missing BASE_SHA) -- skipping.")
        return

    changed_skills = set()
    for f in files:
        m = SKILL_RE.match(f)
        if m:
            changed_skills.add(m.group(1))

    touched_scenario_dirs = set()
    for f in files:
        m = SCENARIO_RE.match(f)
        if m:
            touched_scenario_dirs.add(m.group(1))

    errors = []
    for skill in sorted(changed_skills):
        if skill not in touched_scenario_dirs:
            errors.append(
                f"skills/{skill}/SKILL.md changed but no file under tests/scenarios/{skill}/ "
                f"was touched in this change. CLAUDE.md: a skill change needs a pressure "
                f"scenario demonstrating the skill resists the failure it's meant to prevent."
            )

    if errors:
        print(f"Skill/scenario coverage check failed ({len(errors)} issue(s)):")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)

    print(f"OK: {len(changed_skills)} changed skill(s) each have a touched scenario file.")


if __name__ == "__main__":
    main()
