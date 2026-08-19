---
name: doctor
description: Use when auditing artifact-tree health — cross-reference integrity, orphaned records, stale references to superseded versions — a diagnostic report, not a fix-everything command
---

# doctor

## Overview

A health check for the artifact tree itself: does every cross-reference actually resolve, is
anything referencing a superseded version without acknowledgment, does anything look orphaned.
Complements `/sprout:graph` (which explains relationships for one node) by scanning the whole
tree for integrity problems. Reports findings — doesn't auto-fix, since most fixes here are
judgment calls (which version should this stale reference actually point to?), not mechanical.

**Announce at start:** "I'm using the doctor skill to audit artifact-tree integrity."

## Checks

1. **Dangling references** — does every `implements:`, `design:`, `architecture:` ID on every
   task/requirement/design actually resolve to a file that exists?
2. **Stale version references** — does any task/design reference a requirement ID that currently
   resolves to a `SUPERSEDED` version without the task showing awareness of the newer one (the
   same staleness `develop-next`'s `CHECK STALENESS` step checks per-task, run here across the
   whole tree at once)?
3. **Orphaned approval records** — does every `APR-*.md`'s `artifact:` field point at something
   that still exists?
4. **Schema version drift** — does `.sprout/project.yaml`'s `schema_version` match every
   artifact's expectations, or is there a mix that `migrate` should have reconciled?
5. **R3/R4 tasks without approval** — the same invariant `.github/scripts/check_risk_approval.py`
   enforces in CI for Sprout's own repo; `doctor` runs the equivalent check for a downstream
   project locally, before a PR even exists to run CI against.
6. **Immutable artifacts edited out of band** — if the project has git history, check whether any
   `APR-*`/`RUN-*`/`EVD-*` file, or an already-`APPROVED` requirement/design/decision's body, was
   ever modified after creation (`git log --follow -p` on the file, look for a second commit
   touching body content) — the same thing `hooks/check-immutable-artifacts.py` prevents going
   forward; `doctor` looks backward for anything that slipped through before the hook existed or
   in a project that hasn't installed it.

## Output

One finding per issue: `<file>: <problem>.` Group by check type. Zero findings across all checks
→ `Clean — no integrity issues found.`

## Must not

- Auto-fix a finding without human judgment (most fixes here aren't mechanical)
- Skip the git-history check just because it's slower than the others — it's the one that catches
  a class of problem the other checks can't (something already wrong, not something newly wrong)
