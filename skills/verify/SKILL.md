---
name: verify
description: Use when running a task's verification plan and capturing evidence — dispatches the verifier agent for an independent verdict rather than trusting the implementer's own report, and never lets a task reach VERIFIED without a valid evidence bundle
---

# verify

## Overview

Executes a task's verification plan (`checks:` list on `artifacts/task.md`) against a specific
commit/environment, captures evidence for each check, and records an immutable
`artifacts/verification-run.md`. The implementation agent never produces its own final verdict —
that's the `verifier` agent's job, reading the requirement and acceptance criteria directly.

**Announce at start:** "I'm using the verify skill to run verification for [TASK-XXX]."

## Steps

1. Load the task's verification plan and the requirement's acceptance criteria.
2. Run each required check (lint, unit, integration, contract, build, deploy, security, runtime,
   computer_use, visual, review — only the ones the task's plan actually lists).
3. Capture evidence for each check as `artifacts/evidence.md` records — redact secrets/PII per
   `project.yaml` evidence_policy before storing anything.
4. Dispatch the `verifier` agent with the requirement, acceptance criteria, and captured evidence
   (not the implementer's summary) to judge whether the evidence actually proves the criteria.
5. Record the `artifacts/verification-run.md` — checks, evidence refs, verdict, failure class if
   applicable. Never overwrite a prior run; a retry creates the next `RUN-XXXXXX`.
6. Only on a `PASS` verdict does the task's state advance past `EVIDENCE_CAPTURE`.

## Evidence sufficiency bar

Evidence must prove the acceptance criterion, not just be adjacent to it.
Not sufficient: `HTTP 200` alone. Sufficient: `HTTP 200` + schema validation + required fields
present + expected persisted state. Not sufficient: a screenshot of the UI. Sufficient: a
screenshot that demonstrates the specific expected state the criterion asserts.

## Must not

- Let the implementation agent issue the final verdict on its own work
- Accept "tests passed" as proof of product-intent correctness
- Overwrite a previous verification run
- Store unredacted secrets or unnecessary personal data as evidence
