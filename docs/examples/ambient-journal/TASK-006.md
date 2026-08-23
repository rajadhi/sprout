---
id: TASK-006
title: Enforce dropped location signal is never read by generation
status: RELEASED

implements: [REQ-001]
design: []
architecture: []
acceptance_criteria: [AC-001-04]

size: XS
risk: R2
dependencies: []

github_issue: null
verification_run: RUN-toy-002
approval_ref: APR-00005

created_at: "2026-09-03"
---

## Purpose

Exists specifically because of the REQ-001 v1→v2 supersession — enforces the drop rather than
just relying on new code paths not calling location APIs. Any location-permission code path or
stored location data from a prior build must be inert. No design dependency: this is backend
enforcement, not UI — unlike TASK-009 (retired), this task never depended on a design version.

Implemented and verified for real: `tests/fixtures/toy-app/consent_store.py`,
`tests/fixtures/toy-app/RUN-toy-002.md`, `tests/fixtures/toy-app/EVD-toy-002.md`. Real git
worktree, real subagent-driven TDD, real independent verification — see `RUN-toy-002.md` for the
full account.

## Verification plan

checks:
  - unit
  - security

## Expected evidence

Unit test seeding stale location data from a simulated prior version; assert generation output
contains zero references to it. Security-classed check: no location permission request exists
anywhere in the consent flow (TASK-001/002 scope explicitly excludes it).

## Release

Released 2026-08-23 via `/sprout:release`, real dogfood run of the skill end-to-end
(`docs/protocol.md` §9 backlog item). Candidate: commit `5b85c81` on `origin/main` (PR #6) —
independently confirmed against actual git history, not trusted from this file's own `status:`
field. No staging deploy: `tests/fixtures/toy-app` has no real deployment mechanism, and none was
fabricated. `production_approval_policy: human_required` gate cleared under `APR-00005`.
