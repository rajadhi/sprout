---
name: develop-next
description: Use when selecting and executing the next ready task end to end — worktree, TDD, implementation, local verification, PR — using Superpowers for the mechanics and Sprout for task selection, staleness checks, and the diagnose/retry failure path
---

# develop-next

## Overview

This is Sprout's loop-engineered core: one task travels a self-driving cycle from `READY` to
`PR_OPEN`, stopping only at evidence-gated checkpoints or genuine blockers — not because an agent
decided it's done. Reuses Superpowers for TDD/implementation mechanics rather than reproducing
them; Sprout stays responsible for task selection, staleness, evidence, and state.

**Announce at start:** "I'm using the develop-next skill to select and execute the next task."

## Workflow

```
LOAD PROJECT STATE
→ FIND READY TASKS
→ SELECT ONE TASK              (see selection algorithm below)
→ READ FULL CONTEXT            (requirement, design, ADRs, acceptance criteria)
→ CHECK STALENESS               (has the requirement/design changed since this task was planned?)
→ CREATE ISOLATED WORKTREE/BRANCH   (Superpowers: using-git-worktrees)
→ CREATE IMPLEMENTATION PLAN        (Superpowers: writing-plans)
→ TDD                                (Superpowers: test-driven-development — RED, GREEN, REFACTOR)
→ IMPLEMENT                          (Superpowers: subagent-driven-development where task warrants it)
→ LOCAL VERIFY
→ REQUEST REVIEW                     (Superpowers: requesting-code-review, or implementation-reviewer agent)
→ HAND OFF TO PR                     (Superpowers: finishing-a-development-branch)
```

## Task selection algorithm

Not the oldest or first issue. Evaluate ready tasks on readiness, dependency satisfaction,
priority, value, blocking potential, risk, size, critical-path relevance. Prefer smaller tasks
when value and dependencies are comparable. Conceptually:

```
score = value + blocking_value + readiness + critical_path_weight - risk_penalty - size_penalty
```

Doesn't need to be mathematically precise in v1 — make the policy explicit and let the human
override the pick at any time.

## TDD policy

For application changes: RED (failing test) → GREEN (minimal implementation) → REFACTOR →
regression verification. Do not skip TDD silently. Where TDD doesn't apply (docs-only, static
config, pure design artifacts), the task must document why and what verification is used instead.
Writing tests after implementation and calling it TDD is not acceptable.

## Failure handling (folds in what the original brief called `diagnose`)

On any verification failure, classify it before retrying:
```
SPEC_ERROR  DESIGN_ERROR  IMPLEMENTATION_ERROR  TEST_ERROR  ENVIRONMENT_ERROR
DEPENDENCY_ERROR  UX_ERROR  ACCESSIBILITY_ERROR  SECURITY_ERROR  ARCHITECTURE_ERROR
DATA_ERROR  UNKNOWN
```
Then route per the task state machine's failure paths (`docs/protocol.md` §7):
`VERIFICATION_FAILED → DIAGNOSING → IMPLEMENTING`,
`SPECIFICATION_INVALID → NEEDS_REQUIREMENT_REVIEW`,
`ARCHITECTURE_INVALID → NEEDS_ARCHITECTURE_REVIEW`,
`SECURITY_FAILURE → BLOCKED/HUMAN_REVIEW`,
`ENVIRONMENT_FAILURE → RETRY` — bounded, cap at 2 attempts, never blind-loop.

## Must not

- Select a task without running the selection algorithm
- Skip staleness checks against upstream requirement/design
- Implement without an isolated branch/worktree
- Claim TDD compliance for tests written after the fact
- Produce its own final verification verdict — that's `verify`'s job, not this skill's
