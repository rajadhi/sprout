---
id: TASK-009
title: Remove location option from consent prompt and signal indicator
status: RETIRED

implements: [REQ-001]
design: [DES-001]
architecture: []
acceptance_criteria: [AC-001-04]

size: XS
risk: R1
dependencies: []

github_issue: null
verification_run: null

created_at: "2026-09-03"
retired_at: "2026-09-04"
retirement_reason: >
  Planned on an unchecked assumption -- see docs/examples/ambient-journal/GRAPH-REQ-001.md
  "What changed and why." DES-001-v1 was assumed to reference location because REQ-001-v1
  (which it was built against) had location in scope. Re-running graph's impact analysis for
  real (grepping DES-001-v1.md directly instead of reasoning from the requirement diff) found
  zero location references anywhere in it -- it was written signal-agnostically. There is
  nothing for this task to implement. Retired, not completed and not deleted -- the record of
  why it was planned and why it turned out unnecessary stays, per docs/protocol.md §1.5.
---

<!-- Originally BLOCKED, not READY -- plan's rule 9 correctly withheld READY pending DES-001-v2.
     That gate worked as designed. What it couldn't catch is that the premise underneath the
     block was itself wrong; catching that took an agent actually opening DES-001-v1.md and
     checking, which is exactly what a corrected graph query did. See GRAPH-REQ-001.md. -->

## Purpose (as originally planned — kept for the record, not corrected)

`DES-001`'s consent-prompt flow and signal-indicator component both reference location (written
under REQ-001-v1, before the v1→v2 supersession). This task removes the location-specific UI once
`DES-001-v2` exists — not before, since there is currently nothing to implement against.

**This premise was false.** `DES-001-v1` never referenced location. See
`docs/examples/ambient-journal/GRAPH-REQ-001.md`.

## Verification plan

Not applicable — retired before implementation.

## Expected evidence

Not applicable — retired before implementation.
