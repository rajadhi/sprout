---
name: release
description: Use when moving verified, merged work toward production — enforces project.yaml's production_approval_policy and never lets an agent unilaterally weaken release policy
---

# release

## Overview

Production deployment is a state transition, not an implicit consequence of merging:
`VERIFIED → RELEASE_CANDIDATE → STAGING → PRODUCTION_APPROVAL → RELEASED`. Whether
`PRODUCTION_APPROVAL` needs a human depends entirely on `project.yaml`'s
`production_approval_policy` — this skill enforces whatever that policy says, it never decides to
skip or weaken it.

**Announce at start:** "I'm using the release skill to move [MERGED task/commit] toward
production."

## Steps

1. Confirm every task in this release candidate is `MERGED` with a recorded `VERIFIED` verdict —
   nothing enters a release candidate on the strength of "should be fine."
2. Tag the release candidate (`RELEASE_CANDIDATE`), recording exactly which commits/tasks it
   contains.
3. Deploy to staging (`STAGING`) using the project's actual deployment mechanism — Sprout doesn't
   own or replace this (`docs/protocol.md` §10 non-goals: no custom deployment platform).
4. Run staging verification if the project's verification plan calls for it (e.g. a smoke-test
   scenario against the staging environment) — capture evidence the same way `verify` does.
5. Check `project.yaml`'s `production_approval_policy`:
   - `human_required` → stop, present the release candidate (contents, staging evidence) for
     explicit human approval. Create an `artifacts/approval.md` record. Do not proceed without it.
   - anything else (e.g. an autonomous policy for R0/R1-only releases) → proceed only if every
     task in the candidate is at or below the policy's stated risk ceiling; otherwise stop and
     require human approval anyway, regardless of the general policy setting.
6. On approval (or autonomous clearance), transition to `RELEASED` and record the release —
   which tasks, which commit, when, under what approval.
7. Report exactly what was released and under what authority (human approval ref, or the
   autonomous policy clause that applied).

## Must not

- Release a task that isn't `MERGED` with a `VERIFIED` verdict
- Weaken or bypass `production_approval_policy` — that's a human decision to change, not an
  agent's to route around
- Treat "staging looks fine" as a substitute for the policy's actual approval requirement
- Own or replace the project's real deployment mechanism
