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
#
# from any pre-VERIFIED state -> RETIRED (terminal) when /sprout:graph's impact analysis
# determines this task's planned work no longer applies. Don't delete on retirement — the
# record of why it was planned and why it turned out unnecessary is worth keeping (§1.5).
# retirement_reason: (required if status: RETIRED)

implements: [REQ-XXX]
design: []
architecture: []            # ADR-XXX refs
acceptance_criteria: []      # AC-XXX-NN refs

size: unknown                # XS | S | M | L | XL — L/XL should be decomposed
risk: unknown                 # R0 | R1 | R2 | R3 | R4, see project.yaml autonomy_policy
dependencies: []

github_issue: null
verification_run: null       # RUN-XXXXXX once verified
approval_ref: null            # APR-XXXXX -- required once risk is R3 or R4 (project.yaml
                               # autonomy_policy: human_required/human_controlled). Enforced by
                               # CI (.github/scripts/check_risk_approval.py), not just documented
                               # -- a required status check, since required_pull_request_reviews
                               # alone can't be relied on for a solo-maintainer repo where the
                               # owner can bypass branch protection.

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
