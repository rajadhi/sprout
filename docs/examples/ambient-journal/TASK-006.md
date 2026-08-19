---
id: TASK-006
title: Enforce dropped location signal is never read by generation
status: READY

implements: [REQ-001]
design: []
architecture: []
acceptance_criteria: [AC-001-04]

size: XS
risk: R2
dependencies: []

github_issue: null
verification_run: null

created_at: "2026-09-03"
---

## Purpose

Exists specifically because of the REQ-001 v1→v2 supersession — enforces the drop rather than
just relying on new code paths not calling location APIs. Any location-permission code path or
stored location data from a prior build must be inert. No design dependency: this is backend
enforcement, not UI, so it isn't blocked by TASK-009's DES-001-v2 wait.

## Verification plan

checks:
  - unit
  - security

## Expected evidence

Unit test seeding stale location data from a simulated prior version; assert generation output
contains zero references to it. Security-classed check: no location permission request exists
anywhere in the consent flow (TASK-001/002 scope explicitly excludes it).
