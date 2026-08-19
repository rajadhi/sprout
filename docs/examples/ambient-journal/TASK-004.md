---
id: TASK-004
title: Display empty state when no signals are authorized
status: READY

implements: [REQ-001]
design: [DES-001]
architecture: []
acceptance_criteria: [AC-001-02]

size: XS
risk: R0
dependencies: [TASK-001, TASK-002]

github_issue: null
verification_run: null

created_at: "2026-09-03"
---

## Purpose

Today view shows `DES-001`'s empty state ("Nothing captured yet today.") when zero signals are
authorized — not a blank screen, not a hard error.

## Verification plan

checks:
  - unit
  - visual

## Expected evidence

Screenshot matching `DES-001`'s empty-state spec, captured with zero consent granted.
