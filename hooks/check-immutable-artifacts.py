#!/usr/bin/env python3
"""
PreToolUse hook: enforces docs/protocol.md §1's immutability invariant deterministically, without
needing LLM judgment (docs/architecture.md §5 names this exact kind of check as a hook candidate).

Never rewrite accepted requirements, designs, decisions, verification runs, evidence, or
approvals (protocol.md §1.5). Concretely:

  - APR-*.md / RUN-*.md / EVD-*.md (approval, verification-run, evidence records) are immutable
    the moment they exist on disk -- any Edit/Write to an existing one is denied outright.
  - REQ-*.md / DES-*.md / ADR-*.md / DEC-*.md whose on-disk `status:` is already
    APPROVED/SUPERSEDED/VERIFIED/ACCEPTED may only have their status/supersedes/superseded_by/
    approved_at/approval_ref frontmatter fields changed -- a state-machine transition, not a
    content rewrite. Any body change, or a frontmatter change to any other field, is denied.
    Content changes belong in a new version file instead.
  - Everything else (tasks, intents, not-yet-approved drafts) is unrestricted -- this hook only
    protects the specific artifact types protocol.md §1.5 names as immutable.

Reads a Claude Code PreToolUse hook payload on stdin, exits 0 to allow, exits 2 (writing the
reason to stderr) to block.
"""
import json
import re
import sys
from pathlib import Path

HARD_IMMUTABLE_PREFIXES = ("APR-", "RUN-", "EVD-")
SOFT_IMMUTABLE_PREFIXES = ("REQ-", "DES-", "ADR-", "DEC-")
SOFT_LOCK_STATUSES = {"APPROVED", "SUPERSEDED", "VERIFIED", "ACCEPTED"}
ALLOWED_FIELDS = {"status", "supersedes", "superseded_by", "approved_at", "approval_ref"}

FRONTMATTER_RE = re.compile(r"\A---\n(.*?)\n---\n(.*)\Z", re.DOTALL)


def split_frontmatter(text):
    m = FRONTMATTER_RE.match(text)
    if not m:
        return None, None
    return m.group(1), m.group(2)


def parse_field(frontmatter, key):
    m = re.search(rf"^{key}:\s*(.*)$", frontmatter, re.MULTILINE)
    return m.group(1).strip() if m else None


def changed_field_names(old_fm, new_fm):
    """Line-set diff of frontmatter blocks; returns the set of field names on any changed line."""
    old_lines = set(old_fm.splitlines())
    new_lines = set(new_fm.splitlines())
    changed = old_lines.symmetric_difference(new_lines)
    fields = set()
    for line in changed:
        m = re.match(r"^([A-Za-z_][A-Za-z0-9_]*):", line)
        if m:
            fields.add(m.group(1))
        else:
            # a changed line with no recognizable "key:" prefix (e.g. a multi-line value's
            # continuation) can't be verified safe -- surface as an unknown-field-shaped block
            fields.add("<unparseable-line>")
    return fields


def deny(reason):
    sys.stderr.write(reason + "\n")
    sys.exit(2)


def allow():
    sys.exit(0)


def main():
    try:
        payload = json.load(sys.stdin)
    except Exception:
        # Can't parse the hook payload at all -- fail open rather than block unrelated tool use
        # on a hook-protocol issue that has nothing to do with artifact immutability.
        allow()
        return

    tool_name = payload.get("tool_name")
    tool_input = payload.get("tool_input", {})
    if tool_name not in ("Edit", "Write"):
        allow()
        return

    file_path = tool_input.get("file_path")
    if not file_path:
        allow()
        return

    path = Path(file_path)
    basename = path.name

    is_hard = basename.startswith(HARD_IMMUTABLE_PREFIXES)
    is_soft_candidate = basename.startswith(SOFT_IMMUTABLE_PREFIXES)

    if not (is_hard or is_soft_candidate):
        allow()
        return

    if not path.exists():
        # Creating a new file under one of these prefixes is exactly how new versions/records
        # are supposed to come into existence -- only *editing an existing one* is restricted.
        allow()
        return

    original_text = path.read_text()

    if is_hard:
        deny(
            f"{file_path}: this is an immutable record (approval/verification-run/evidence) per "
            f"docs/protocol.md §1.5. It cannot be edited once created -- create a new ID instead."
        )
        return

    # Soft-immutable candidate: only locked once its current on-disk status says so.
    old_fm, old_body = split_frontmatter(original_text)
    if old_fm is None:
        # No parseable frontmatter yet -- not something this hook can protect; let it through
        # rather than guessing.
        allow()
        return

    current_status = (parse_field(old_fm, "status") or "").upper()
    if current_status not in SOFT_LOCK_STATUSES:
        allow()
        return

    if tool_name == "Edit":
        old_string = tool_input.get("old_string", "")
        new_string = tool_input.get("new_string", "")
        new_text = original_text.replace(old_string, new_string, 1)
    else:  # Write
        new_text = tool_input.get("content", "")

    new_fm, new_body = split_frontmatter(new_text)
    if new_fm is None:
        deny(
            f"{file_path}: this edit would remove/corrupt the frontmatter of an already-"
            f"{current_status} artifact. Denied -- immutable once approved, per docs/protocol.md §1.5."
        )
        return

    if new_body != old_body:
        deny(
            f"{file_path}: this edit changes body content on an already-{current_status} "
            f"artifact. Immutable once approved (docs/protocol.md §1.5) -- create a new version "
            f"file instead of editing this one."
        )
        return

    changed = changed_field_names(old_fm, new_fm)
    offending = changed - ALLOWED_FIELDS
    if offending:
        deny(
            f"{file_path}: this edit changes frontmatter field(s) {sorted(offending)} on an "
            f"already-{current_status} artifact. Only {sorted(ALLOWED_FIELDS)} may change after "
            f"approval (state-machine transitions), per docs/protocol.md §1.5."
        )
        return

    allow()


if __name__ == "__main__":
    main()
