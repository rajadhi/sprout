---
name: plan
description: Use when converting accepted requirements and designs into small vertical-slice tasks — decomposes by user-visible behaviour rather than technical layer, and creates GitHub issues automatically once a task reaches READY
---

# plan

## Overview

Reads accepted requirements/designs/ADRs and produces small, independently verifiable tasks
(`artifacts/task.md`). Does not implement application code. Includes what the original brief
called `sync-github` — issue creation is automatic here, not a separate step, because a task
reaching `READY` and a GitHub issue existing for it are the same event.

**Announce at start:** "I'm using the plan skill to decompose [REQ-XXX / feature] into tasks."

## Steps

1. Read the current artifact graph (`/sprout:graph`-equivalent traversal).
2. Find accepted (`APPROVED`) requirements without full task coverage.
3. Read accepted designs and relevant ADRs.
4. Determine dependencies between prospective tasks.
5. Identify implementation gaps against what already exists in the codebase.
6. Decompose work into small tasks — **vertical slices**, not technical layers.
7. Assign size (XS-XL) and risk (R0-R4, per `project.yaml` autonomy_policy).
8. Generate each task's verification plan (`checks:` list) and expected evidence.
9. Mark a task `READY` only when its prerequisites are satisfied.
10. For every task that reaches `READY`: create a GitHub issue, apply `sprout:*` labels
    (type/state/risk/size — see `docs/architecture.md`), and record the issue number on the task.
    Never rewrite an existing issue's history — update metadata, don't recreate.

## Decomposition rule

Prefer:
```
user-visible behaviour + minimum required backend + minimum required tests
```
over technical-layer decomposition (database / API / service / UI / tests as separate tasks).
Bad: "database, API, service, UI, tests" as 5 tasks for one feature.
Good: "create journal day, display empty journal, attach one photo, generate one draft" as 4
independently releasable tasks.

A task is too large when it has multiple unrelated outcomes, needs multiple independent review
decisions, can't be verified with one coherent plan, has several independently releasable
behaviours, or reverting it would require disentangling unrelated changes. `L`/`XL` should
normally be decomposed further; `XL` must never be marked `READY` for autonomous execution.

## Must not

- Implement application code
- Mark a task `READY` before its dependencies are satisfied
- Treat GitHub issue text as canonical — the task artifact is canonical, GitHub is a projection
