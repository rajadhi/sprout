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


def check_hooks_manifest():
    path = ROOT / "hooks" / "hooks.json"
    if not path.exists():
        return
    try:
        data = json.loads(path.read_text())
    except Exception as e:
        errors.append(f"{path}: invalid JSON ({e})")
        return
    if "hooks" not in data:
        errors.append(f"{path}: missing top-level 'hooks' field")
        return
    for event, matchers in data["hooks"].items():
        for matcher_entry in matchers:
            for hook in matcher_entry.get("hooks", []):
                command = hook.get("command", "")
                script_ref = command.replace("${CLAUDE_PLUGIN_ROOT}", str(ROOT))
                for token in script_ref.split():
                    token = token.strip('"')
                    if token.startswith(str(ROOT)) and not Path(token).exists():
                        errors.append(f"{path}: {event} hook references missing file {token}")


def main():
    check_plugin_manifest()
    check_hooks_manifest()

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
