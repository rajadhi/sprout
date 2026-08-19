---
id: TASK-003
title: Revoke a granted signal's consent takes effect immediately
status: READY

implements: [REQ-003]
design: [DES-001]
architecture: []
acceptance_criteria: [AC-003-02]

size: S
risk: R2
dependencies: [TASK-001, TASK-002]

github_issue: null
verification_run: null

created_at: "2026-09-03"
---

## Purpose

Settings → Signals lets the user revoke either signal independently. Revocation must be effective
immediately — no cached data from before revocation may be used by a later generation.

## Verification plan

checks:
  - unit
  - integration

## Expected evidence

Integration test: revoke photo consent mid-session, trigger generation, assert no photo data
appears — not just "no new photo reads," but no reuse of anything cached from before revocation.
