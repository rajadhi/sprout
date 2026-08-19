---
id: TASK-007
title: Inline edit of draft text persists
status: READY

implements: [REQ-002]
design: [DES-001]
architecture: []
acceptance_criteria: [AC-002-01]

size: S
risk: R1
dependencies: [TASK-005]

github_issue: null
verification_run: null

created_at: "2026-09-03"
---

## Purpose

Tap-to-edit on the draft text block per `DES-001`'s interaction model — no separate edit-mode
toggle. Saved edit replaces the draft's stored content.

## Verification plan

checks:
  - unit
  - integration

## Expected evidence

Integration test: edit text, save, force-close app, reopen, assert edited text shown (not
original generation).
