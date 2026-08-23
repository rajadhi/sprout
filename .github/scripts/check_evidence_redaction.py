#!/usr/bin/env python3
"""
Deterministic CI check: every committed evidence record must declare a redaction_state other
than "unredacted", and must not contain an obviously secret-shaped string regardless of what it
declares.

Why this exists: artifacts/evidence.md and skills/verify/SKILL.md both instruct redacting
secrets/PII before storing evidence, but nothing verified it actually happened -- an agent could
mark redaction_state: redacted without having redacted anything. This gives that instruction real
teeth as a required status check, the same pattern check_risk_approval.py uses for R3/R4
approval: don't trust the self-report, verify it.

Scans every *.md file in the repo whose frontmatter has `id: EVD-*` (excluding the literal
artifacts/evidence.md template, id EVD-XXXXXX) -- not diff-based, a whole-repo invariant, same
style as validate_structure.py and check_risk_approval.py.
"""
import os
import re
import sys
from pathlib import Path

ROOT = Path(os.environ.get("SPROUT_CHECK_ROOT") or Path(__file__).resolve().parents[2])
FRONTMATTER_RE = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)

SECRET_PATTERNS = [
    ("AWS access key", re.compile(r"AKIA[0-9A-Z]{16}")),
    ("bearer token", re.compile(r"[Bb]earer\s+[A-Za-z0-9\-\._~+/]{20,}")),
    ("password assignment", re.compile(r"(?i)password[\"']?\s*[:=]\s*[\"'][^\"'\s]{4,}[\"']")),
    (
        "api key / secret / token assignment",
        re.compile(
            r"(?i)(api[_-]?key|secret|access[_-]?token)[\"']?\s*[:=]\s*[\"'][A-Za-z0-9\-_]{16,}[\"']"
        ),
    ),
]

errors = []


def parse_field(frontmatter, key):
    m = re.search(rf"^{key}:\s*(.*)$", frontmatter, re.MULTILINE)
    return m.group(1).strip() if m else None


def find_evidence_files():
    for path in ROOT.rglob("*.md"):
        if ".git" in path.parts:
            continue
        text = path.read_text(errors="ignore")
        m = FRONTMATTER_RE.match(text)
        if not m:
            continue
        evd_id = parse_field(m.group(1), "id") or ""
        if not evd_id.startswith("EVD-") or evd_id == "EVD-XXXXXX":
            continue
        yield path, m.group(1), text


def main():
    for path, frontmatter, full_text in find_evidence_files():
        redaction_state = (parse_field(frontmatter, "redaction_state") or "").strip()

        if redaction_state == "unredacted":
            errors.append(
                f"{path}: redaction_state is 'unredacted'. artifacts/evidence.md requires "
                f"redaction before storing -- set to 'redacted' or 'not_applicable'."
            )
            continue

        for label, pattern in SECRET_PATTERNS:
            if pattern.search(full_text):
                errors.append(
                    f"{path}: declares redaction_state '{redaction_state}' but contains what "
                    f"looks like a {label}. Redact it before committing this evidence."
                )
                break

    if errors:
        print(f"Evidence redaction check failed ({len(errors)} issue(s)):")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)

    print(
        "OK: every evidence record is redacted (or not_applicable) with no obvious "
        "secret-shaped strings."
    )


if __name__ == "__main__":
    main()
