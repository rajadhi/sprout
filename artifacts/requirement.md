---
id: REQ-XXX
version: 1
type: unknown                 # product | ux | engineering | constraint
title: unknown
status: PROPOSED              # PROPOSED | SHAPING | READY_FOR_REVIEW | APPROVED | SUPERSEDED | RETIRED
shaping_status: unknown        # only meaningful while status: SHAPING — e.g. needs_input
source_intent: [INT-XXXX]
supersedes: null                # REQ-XXX vN, or null
superseded_by: null
created_at: unknown
approved_at: null
approval_ref: null              # APR-XXXXX once approved
---

<!--
Immutable once APPROVED. A later change creates REQ-XXX v(N+1) with
supersedes/superseded_by set on both versions — never edit this file in place
after approval. Classify new input against this requirement as one of:
NEW, CLARIFICATION, REFINEMENT, SUPERSESSION, CONTRADICTION, DEPRECATION,
BUG, CONSTRAINT, QUESTION — a BUG means this requirement is still correct and
the implementation is wrong; it does not get a new requirement version.
-->

## Problem

## Desired outcome

## Scope

## Non-goals

## Assumptions

## Unknowns

## Acceptance criteria

<!-- Given/When/Then or equivalent testable assertions. Reject vague criteria
     ("should feel intuitive") unless paired with a concrete observable assertion. -->

- AC-XXX-01:

## Dependencies

## UX implications

## Architecture implications

## Security implications

## Privacy implications

## Accessibility implications

## Verification strategy
