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
   - If decomposition surfaces a consequential technical decision not yet covered by an existing
     ADR (data model shape, external dependency choice, security boundary, migration approach),
     draft `artifacts/decision.md` and dispatch the `architecture-reviewer` agent before treating
     it as settled. Don't force an ADR for a trivial implementation choice.
5. Identify implementation gaps against what already exists in the codebase.
6. Decompose work into small tasks — **vertical slices**, not technical layers.
7. Assign size (XS-XL) and risk (R0-R4, per `project.yaml` autonomy_policy).
8. Generate each task's verification plan (`checks:` list) and expected evidence.
9. Mark a task `READY` only when its prerequisites are satisfied.
10. For every task that reaches `READY`: ensure the `sprout:*` label set exists (`gh label create
    --force` is idempotent, safe to run every time), create a GitHub issue via `gh issue create`
    with type/state/risk/size labels and a body pointing back to the canonical task artifact — not
    a copy of its content — and record the returned issue number on the task's `github_issue:`
    field. See `docs/architecture.md` §7 for the exact label set and command shape. On later state
    changes, update labels via `gh issue edit --add-label/--remove-label`; never close and
    recreate an issue, and never treat the issue body as something to keep rewriting — it's a
    pointer, not the content.

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
