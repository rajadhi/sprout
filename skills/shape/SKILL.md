---
name: shape
description: Use when turning raw human input (notes, meeting summaries, sketches, feedback) into structured, reviewable requirements — classifies against existing requirements, detects contradictions, and never invents facts to fill unknowns
---

# shape

## Overview

The primary human-to-structured-intent workflow. Input is raw and messy; output is
proposed requirement versions ready for human approval. This skill never creates GitHub issues —
that only happens once a requirement is approved and later decomposed by `plan`.

**Announce at start:** "I'm using the shape skill to turn this input into proposed requirements."

## Workflow

```
INGEST
→ CLASSIFY        (NEW, CLARIFICATION, REFINEMENT, SUPERSESSION, CONTRADICTION,
                    DEPRECATION, BUG, CONSTRAINT, or QUESTION against existing requirements)
→ FIND RELATED ARTIFACT-GRAPH NODES
→ IDENTIFY NEW INFORMATION
→ DETECT CONTRADICTIONS
→ FORMULATE INTERPRETATION
→ IDENTIFY UNKNOWNS
→ GENERATE REQUIREMENTS       (using artifacts/requirement.md)
→ GENERATE ACCEPTANCE CRITERIA
→ GENERATE VERIFICATION STRATEGY
→ CRITIQUE                    (dispatch to specification-critic agent)
→ PRESENT FOR APPROVAL
```

## Classification rules

- **Clarification** — no meaningful change in intent. May create a new version but must not
  invalidate downstream implementation unnecessarily.
- **Refinement** — adds precision; may require design/test changes.
- **Supersession** — changes intended behaviour. Must trigger impact analysis (`/sprout:graph`).
- **Contradiction** — conflicts with an active requirement. Do not resolve silently — present both
  interpretations to the human.
- **Bug** — the requirement remains correct; the implementation is wrong. Do not create a new
  product requirement merely because code is defective — route to `develop-next`'s diagnose path
  instead.

## Acceptance criteria bar

Reject criteria like "the experience should feel intuitive" unless paired with a concrete,
observable assertion. Prefer Given/When/Then or equivalent precision. Every accepted requirement
needs at least one acceptance criterion, except explicit non-functional constraints with a
documented measurable form.

## Approval

Present: what changed, why, what's new, what's superseded, unknowns, downstream impact. The human
responds APPROVE / REJECT / CLARIFY / EDIT. Approval creates an immutable `artifacts/approval.md`
record — never treat chat history itself as the approval.

## Must not

- Invent facts to resolve unknowns
- Silently resolve a contradiction
- Create a new requirement version for what is actually a bug
- Generate GitHub issues
