---
id: TASK-009
title: Remove location option from consent prompt and signal indicator
status: BLOCKED

implements: [REQ-001]
design: [DES-001]
architecture: []
acceptance_criteria: [AC-001-04]

size: XS
risk: R1
dependencies: [DES-001-v2]

github_issue: null
verification_run: null

created_at: "2026-09-03"
---

<!-- Deliberately left BLOCKED rather than READY — this is plan's rule 9 ("mark a task READY only
     when its prerequisites are satisfied") holding under real pressure. DES-001 is still v1: its
     consent-prompt copy and signal-indicator component were written when location was in scope
     (REQ-001-v1) and still describe it. TASK-006 already enforces the backend drop without any
     design dependency — this task is the UI cleanup, and it genuinely cannot be verified against
     a design spec that doesn't exist yet. -->

## Purpose

`DES-001`'s consent-prompt flow and signal-indicator component both reference location (written
under REQ-001-v1, before the v1→v2 supersession). This task removes the location-specific UI once
`DES-001-v2` exists — not before, since there is currently nothing to implement against.

## Verification plan

checks:
  - visual
  - review

## Expected evidence

Not yet determinable — depends on what `DES-001-v2` actually specifies for the reduced
signal-indicator states.

## Blocked on

`DES-001-v2` does not exist yet. Per the impact analysis recorded in `APR-00003` and
`docs/examples/ambient-journal/README.md`: `/sprout:graph`-style impact classified `DES-001` as
`NEEDS_REVIEW`, not `INVALIDATED` — the design's flow structure holds, only this specific UI
element needs updating. Running `design` again against `REQ-001-v2` produces `DES-001-v2` and
unblocks this task.
