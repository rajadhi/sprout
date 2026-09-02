---
id: TASK-201
title: Migrate export endpoint's rate limiter to the shared Redis cluster
status: MERGED
implements: [REQ-201]
size: M
risk: R2
verification_run: RUN-00201
approval_ref: null
created_at: 2026-02-05
---

## Purpose

Move rate-limit counters off the export service's local memory onto the shared Redis cluster so
counters survive a pod restart.

## Verification plan

checks:
  - lint
  - unit
  - integration
