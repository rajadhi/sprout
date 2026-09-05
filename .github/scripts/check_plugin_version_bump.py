#!/usr/bin/env python3
"""
Deterministic CI check: a PR that touches significant plugin content (skills, agents, hooks, CI
scripts/workflows, artifact templates, CODEOWNERS) must also bump .claude-plugin/plugin.json's
version -- any increase (patch, minor, or major) counts; which tier is a human/agent judgment
call this check doesn't make, see CLAUDE.md's "Framework governance" section.

Why this exists: this repo hit the same real failure twice (bd0afea, then again the PR that
added skills/upgrade/SKILL.md) -- real feature content shipped without bumping the version,
so Claude Code's plugin manager saw "already installed, nothing changed" and never refreshed a
user's installation, even after an explicit marketplace/plugin update and a forced reload. A
human remembering to bump a version field by convention alone had already failed twice; this
makes it a required status check instead, the same pattern check_risk_approval.py and
check_skill_scenario_coverage.py already use for a convention that needed real teeth.

Changed files come from `git diff --name-only BASE_SHA HEAD_SHA` (BASE_SHA/HEAD_SHA set by the
workflow) or SPROUT_CHANGED_FILES as a direct override for tests/manual runs. The old and new
version strings are read via `git show BASE_SHA:.claude-plugin/plugin.json` and the current
working-tree file, unless SPROUT_OLD_VERSION/SPROUT_NEW_VERSION override them (tests).
"""
import json
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(os.environ.get("SPROUT_CHECK_ROOT") or Path(__file__).resolve().parents[2])
PLUGIN_JSON = "plugin.json" if (ROOT / "plugin.json").exists() else ".claude-plugin/plugin.json"

# Paths that constitute real plugin behavior or schema -- a change here is exactly the class of
# change that silently shipped without a version bump twice before. Deliberately excludes docs/
# and tests/ on their own: a docs-only fix or a new pressure scenario with no accompanying
# skill/script change isn't the failure mode this check exists to catch.
SIGNIFICANT_PREFIXES = (
    "skills/", "agents/", "hooks/", ".github/scripts/", ".github/workflows/", "artifacts/",
    "CODEOWNERS",
)


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


def parse_version(text):
    try:
        version = json.loads(text).get("version", "")
    except Exception:
        return None
    m = re.match(r"^(\d+)\.(\d+)\.(\d+)", version.strip())
    return tuple(int(g) for g in m.groups()) if m else None


def old_version():
    override = os.environ.get("SPROUT_OLD_VERSION")
    if override is not None:
        return parse_version(json.dumps({"version": override}))
    base_sha = os.environ.get("BASE_SHA")
    if not base_sha or set(base_sha) == {"0"}:
        return None
    result = subprocess.run(
        ["git", "show", f"{base_sha}:{PLUGIN_JSON}"], capture_output=True, text=True, cwd=ROOT
    )
    return parse_version(result.stdout) if result.returncode == 0 else None


def new_version():
    override = os.environ.get("SPROUT_NEW_VERSION")
    if override is not None:
        return parse_version(json.dumps({"version": override}))
    path = ROOT / PLUGIN_JSON
    return parse_version(path.read_text()) if path.exists() else None


def main():
    files = changed_files()
    if files is None:
        print("OK: no base to diff against (new branch or missing BASE_SHA) -- skipping.")
        return

    significant = [f for f in files if any(f.startswith(p) for p in SIGNIFICANT_PREFIXES)]
    if not significant:
        print("OK: no significant plugin paths changed -- no version bump required.")
        return

    old = old_version()
    new = new_version()

    if new is None:
        print(f"Plugin version check failed: could not read a version from {PLUGIN_JSON}.")
        sys.exit(1)

    if old is not None and new <= old:
        print(
            f"Plugin version check failed: significant plugin path(s) changed "
            f"({', '.join(significant[:5])}{'...' if len(significant) > 5 else ''}) but "
            f"{PLUGIN_JSON}'s version did not increase ({'.'.join(map(str, old))} -> "
            f"{'.'.join(map(str, new))}). Bump the patch version by default; bump minor/major "
            f"only when explicitly asked (see CLAUDE.md's Framework governance section)."
        )
        sys.exit(1)

    print(f"OK: significant plugin path(s) changed and version increased to {'.'.join(map(str, new))}.")


if __name__ == "__main__":
    main()
