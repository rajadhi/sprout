---
id: TASK-001
title: Request and store photo-signal consent
status: READY

implements: [REQ-003]
design: [DES-001]
architecture: []
acceptance_criteria: [AC-003-01, AC-003-03]

size: S
risk: R1
dependencies: []

github_issue: 8   # github.com/rajadhi/sprout/issues/8, real, kept open (not a throwaway test issue)
verification_run: null

created_at: "2026-09-03"
---

## Purpose

First time a photo is relevant, show the photo-specific consent prompt from `DES-001`; on accept,
store consent; on decline, store decline and don't ask again unless the user revisits Settings.

## Verification plan

checks:
  - unit
  - integration

## Expected evidence

Unit test: consent state persists across app restart. Integration test: prompt text matches
`DES-001` Copy rules (specific purpose, not generic "Allow Photos Access").
