#!/usr/bin/env python3
"""
Deterministic structural validation for Sprout's own repo (docs/architecture.md §5: hooks are
for enforcement that doesn't need LLM judgment). Not a linter for downstream projects' code --
this only checks that Sprout's own plugin files are structurally sound: valid plugin manifest,
every skill/agent has the frontmatter Claude Code needs to load it.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FRONTMATTER_RE = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)

errors = []


def check_plugin_manifest():
    path = ROOT / ".claude-plugin" / "plugin.json"
    try:
        data = json.loads(path.read_text())
    except Exception as e:
        errors.append(f"{path}: invalid JSON ({e})")
        return
    for field in ("name", "version", "description"):
        if field not in data:
            errors.append(f"{path}: missing required field '{field}'")


def check_frontmatter(path, required_fields=("name", "description")):
    text = path.read_text()
    m = FRONTMATTER_RE.match(text)
    if not m:
        errors.append(f"{path}: missing YAML frontmatter (must start with '---')")
        return
    body = m.group(1)
    for field in required_fields:
        if not re.search(rf"^{field}:", body, re.MULTILINE):
            errors.append(f"{path}: frontmatter missing '{field}:' field")


def main():
    check_plugin_manifest()

    for skill_file in sorted((ROOT / "skills").glob("*/SKILL.md")):
        check_frontmatter(skill_file)

    for agent_file in sorted((ROOT / "agents").glob("*.md")):
        check_frontmatter(agent_file)

    if errors:
        print(f"Structural validation failed ({len(errors)} issue(s)):")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)

    skill_count = len(list((ROOT / "skills").glob("*/SKILL.md")))
    agent_count = len(list((ROOT / "agents").glob("*.md")))
    print(f"OK: plugin manifest valid, {skill_count} skills, {agent_count} agents all have required frontmatter.")


if __name__ == "__main__":
    main()
