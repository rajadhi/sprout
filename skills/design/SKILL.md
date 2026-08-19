---
name: design
description: Use when producing or revising UX/UI design for approved requirements — self-critiques via ux-critic and accessibility-critic before presenting an approval-ready candidate, never asking the human to review every iteration
---

# design

## Overview

Turn accepted requirement(s) into a critiqued, approval-ready design candidate. The design loop
self-critiques first; the human is not asked to review every intermediate iteration.

**Announce at start:** "I'm using the design skill to produce a design candidate for [REQ-XXX]."

## Workflow

```
READ REQUIREMENTS
→ READ EXISTING DESIGN SYSTEM
→ READ PLATFORM CONTEXT           (project.yaml platforms/accessibility_target)
→ UNDERSTAND USER TASK
→ GENERATE DESIGN                  (using artifacts/design.md)
→ CRITIQUE USABILITY               (dispatch ux-critic agent)
→ CRITIQUE ACCESSIBILITY           (dispatch accessibility-critic agent)
→ REVIEW EDGE STATES               (empty, loading, error)
→ REVISE
→ RE-EVALUATE
→ PRESENT APPROVED-QUALITY DESIGN
```

If no specialized visual rendering mechanism is available, work from accessible design artifacts
and runtime screenshots rather than skipping the visual/edge-state review.

## Approval gate

Human approval happens only when: design quality gate passes AND acceptance criteria are
represented AND accessibility review passes. The human then responds APPROVE / REQUEST CHANGES /
REJECT. Approved design versions are immutable — a later change creates the next `DES-XXX` version.

## Must not

- Present a design for approval that hasn't passed both critics
- Ask for human review on every iteration
- Skip edge states (empty/loading/error) because they're less visually interesting
