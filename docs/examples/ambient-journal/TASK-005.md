---
id: TASK-005
title: Generate end-of-day draft from photo and calendar signals
status: READY

implements: [REQ-001]
design: [DES-001]
architecture: [ADR-001]
acceptance_criteria: [AC-001-01, AC-001-03]

size: M
risk: R2
dependencies: [TASK-001, TASK-002]

github_issue: null
verification_run: null

created_at: "2026-09-03"
---

## Purpose

Implements both paths from `ADR-001`: the primary background-scheduled trigger and the foreground
fallback backfill, since AC-001-01 must hold even when the background path never fires.

## Verification plan

checks:
  - unit
  - integration
  - runtime

## Expected evidence

Two runtime scenarios: (1) background trigger fires normally, draft generated, references at
least one photo-derived and one calendar-derived detail (AC-001-01), tone check against AC-001-03.
(2) background trigger assumed not to have fired, app opened next day, foreground fallback
backfills the missing day's draft — proving `ADR-001`'s trade-off is actually load-bearing, not
just documented.
