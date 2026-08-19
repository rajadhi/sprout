# Real `/sprout:doctor` output — Ambient Journal fixture

Every check below ran for real against this directory's actual files, not a description of what
the checks would find.

```
1. Dangling references
   Checked: implements:/design:/architecture: on every TASK-*.md
   Referenced IDs: REQ-001, REQ-002, REQ-003, DES-001, ADR-001
   All resolve to real files. Clean.

2. Stale version references
   REQ-001 references resolve to the current APPROVED version (v2) project-wide -- no task
   references a version-pinned "REQ-001-v1" directly (task frontmatter uses the unversioned
   "REQ-001", which is intentionally how staleness gets checked live, per
   skills/develop-next/SKILL.md's CHECK STALENESS step -- see tests/scenarios/develop-next/
   stale-requirement.md). Clean, no action needed beyond what's already been done (TASK-009).

3. Orphaned approval records
   APR-00001 -> [REQ-001-v1, REQ-002-v1, REQ-003-v1]  all exist
   APR-00002 -> DES-001-v1                             exists
   APR-00003 -> REQ-001-v2                             exists
   APR-00004 -> ADR-001                                exists
   Clean.

4. Schema version drift
   artifacts/project.yaml: schema_version: 1
   docs/examples/ambient-journal/project.yaml: schema_version: 1
   docs/examples/init-dogfood/project.yaml: schema_version: 1
   Consistent. Clean.

5. R3/R4 tasks without approval
   Highest risk in this fixture is R2 (TASK-003, TASK-005, TASK-006). No R3/R4 tasks exist.
   Not applicable -- nothing to check.

6. Immutable artifacts edited out of band
   git log --follow -p on REQ-001-v1.md shows exactly one commit, already containing
   status: SUPERSEDED -- the status transition happened before the file was ever committed
   (single authoring session), so there's no multi-commit history to inspect for a body edit
   after an APPROVED commit. Honest limitation: this fixture's git history doesn't span enough
   real time to meaningfully exercise this specific check -- a real project's history would.
   No violation found, but also not a strong test of this check.
```

## Verdict

5 of 6 checks clean with real findings behind them. Check 6 passed trivially rather than
meaningfully — noted rather than claimed as a strong pass.

## How this was actually computed

```bash
grep -h "^implements:\|^design:\|^architecture:" TASK-*.md
grep "^id:" REQ-*.md DES-*.md ADR-*.md
grep "^artifact:" APR-*.md
grep "^schema_version:" artifacts/project.yaml docs/examples/*/project.yaml
git log --follow -p -- docs/examples/ambient-journal/REQ-001-v1.md
```
