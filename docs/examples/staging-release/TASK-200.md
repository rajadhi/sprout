---
id: TASK-200
title: Cache export endpoint responses for 60s
status: RELEASED
implements: [REQ-200]
size: XS
risk: R1
verification_run: RUN-00200
approval_ref: null
created_at: 2026-02-01
---

## Purpose

Reduce load on the export endpoint's downstream dependency for repeated identical requests.

## Verification plan

checks:
  - lint
  - unit
