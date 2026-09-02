---
id: TASK-100
title: Add rate limiting to the export endpoint
status: MERGED
implements: [REQ-100]
size: S
risk: R1
verification_run: RUN-00100
approval_ref: null
created_at: 2026-01-10
---

## Purpose

Prevent a single client from exhausting the export endpoint's downstream quota.

## Verification plan

checks:
  - lint
  - unit
