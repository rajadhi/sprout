---
id: TASK-008
title: Edited entry is not overwritten on signal reprocessing
status: READY

implements: [REQ-002]
design: []
architecture: []
acceptance_criteria: [AC-002-02]

size: XS
risk: R1
dependencies: [TASK-007]

github_issue: null
verification_run: null

created_at: "2026-09-03"
---

## Purpose

If the same day's signals are reprocessed for any reason (retry after TASK-005's foreground
fallback fires, for instance), a user's prior edit must not be silently replaced by a fresh
generation.

## Verification plan

checks:
  - unit

## Expected evidence

Unit test: edit an entry, trigger reprocessing of that day's signals, assert stored content is
still the user's edit, not regenerated text.
