---
id: TASK-002
title: Request and store calendar-signal consent
status: READY

implements: [REQ-003]
design: [DES-001]
architecture: []
acceptance_criteria: [AC-003-01, AC-003-03]

size: S
risk: R1
dependencies: []

github_issue: null
verification_run: null

created_at: "2026-09-03"
---

## Purpose

Same as TASK-001, for the calendar signal. Kept as a separate task rather than folded into
TASK-001 because each signal's consent is independently revocable and independently testable
(AC-003-01/02 apply per-signal) — bundling them would mean one failing test blocks both.

## Verification plan

checks:
  - unit
  - integration

## Expected evidence

Unit test: consent state persists independently of photo consent state. Integration test: prompt
text is calendar-specific, not reused photo copy.
