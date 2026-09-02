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
7. **GitHub Issue drift** — for every task with a non-null `github_issue:` field, compare its
   local state against the live issue (`gh issue list --state all --json number,state,labels`,
   matched against each task's issue number — one call for the whole tree, not one `gh` call per
   task). The local artifact is the source of truth (`docs/architecture.md` §7: GitHub is "a
   projection surface, not the source of truth") — this check exists to find where the projection
   has drifted from what it should be projecting, never to pull GitHub's state back into the
   local artifact. Flag:
   - The issue's `sprout:state:*` label doesn't match the task's actual `status` (mapped per
     `docs/architecture.md` §7's label table — e.g. a task at `VERIFIED` whose issue still carries
     `sprout:state:in-progress`).
   - The issue's `sprout:risk:*` or `sprout:size:*` label doesn't match the task's current
     `risk`/`size` field.
   - The issue is closed but the task's `status` is anything before `VERIFIED` (closed with no
     corresponding local completion is drift worth a human's attention, not necessarily a bug —
     maybe the issue was closed by mistake, maybe the task was actually abandoned and the local
     artifact never got a `RETIRED` transition; `doctor` can't tell which, so it reports both as
     equally plausible rather than picking one).
   - The task's `github_issue:` field points at an issue number that doesn't exist (or isn't in
     this repo) — same "dangling reference" shape as check 1, just against GitHub instead of the
     local tree.

## Output

One finding per issue: `<file>: <problem>.` Group by check type. Zero findings across all checks
→ `Clean — no integrity issues found.`

Check 7's findings additionally carry a **reconciliation patch** — the exact `gh issue edit
<N> --add-label ... --remove-label ...` (or `gh issue reopen`/`gh issue close --comment ...`)
command that would bring the issue back in line with the local artifact. Print the command; never
run it. The patch always targets GitHub — there is no corresponding "patch the local task file"
form, because the local artifact is what the patch is correcting the issue *to match*, not
something check 7 ever has reason to change.

## Must not

- Auto-fix a finding without human judgment (most fixes here aren't mechanical)
- Skip the git-history check just because it's slower than the others — it's the one that catches
  a class of problem the other checks can't (something already wrong, not something newly wrong)
- Run any `gh issue edit`/`close`/`reopen` command check 7 produces — print the patch, never apply
  it, same as every other finding in this skill
- Treat a GitHub issue's live label or state as authoritative over the local task artifact when
  they disagree — check 7 exists to find drift *from* the local artifact, never to import GitHub's
  state as a correction to it
