---
id: TASK-XXX
title: unknown
status: READY
# READY -> CLAIMED -> IMPLEMENTING -> LOCAL_VERIFICATION -> PR_OPEN ->
# CI_VERIFICATION -> RUNTIME_VERIFICATION -> EVIDENCE_CAPTURE ->
# INDEPENDENT_REVIEW -> VERIFIED -> MERGED -> RELEASED
#
# failure paths:
# VERIFICATION_FAILED -> DIAGNOSING -> IMPLEMENTING
# SPECIFICATION_INVALID -> NEEDS_REQUIREMENT_REVIEW
# ARCHITECTURE_INVALID -> NEEDS_ARCHITECTURE_REVIEW
# SECURITY_FAILURE -> BLOCKED / HUMAN_REVIEW
# ENVIRONMENT_FAILURE -> RETRY (bounded, cap 2 — never blind-loop)

implements: [REQ-XXX]
design: []
architecture: []            # ADR-XXX refs
acceptance_criteria: []      # AC-XXX-NN refs

size: unknown                # XS | S | M | L | XL — L/XL should be decomposed
risk: unknown                 # R0 | R1 | R2 | R3 | R4, see project.yaml autonomy_policy
dependencies: []

github_issue: null
verification_run: null       # RUN-XXXXXX once verified

created_at: unknown
---

## Purpose

## Verification plan

<!-- flat list of required checks for this task — not every task needs every
     check. Pick from: lint, unit, integration, contract, build, deploy,
     security, runtime, computer_use, visual, review -->

checks:
  -

## Expected evidence

<!-- what will prove the acceptance criteria — see artifacts/evidence.md -->
