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
→ FIND READY TASKS                  (status: READY only — BLOCKED/etc. never enter this pool)
→ SELECT ONE TASK              (see selection algorithm below)
→ CHECK PROGRESS LOG           (resume vs fresh start — see Progress log and resuming below)
→ READ CONTEXT                  (digest of requirement, design, ADRs, acceptance criteria — see
                                Reading context below; skip if resuming past this phase)
→ CHECK STALENESS               (see below — always runs, even on resume)
→ CREATE ISOLATED WORKTREE/BRANCH   (Superpowers: using-git-worktrees)             [log phase]
→ CREATE IMPLEMENTATION PLAN        (Superpowers: writing-plans)
→ CAPTURE BASELINE                  (record which tests are already red before touching anything)
                                     [log phase]
→ TDD                                (Superpowers: test-driven-development — RED, GREEN, REFACTOR)
                                     [log phase per RED/GREEN commit]
→ IMPLEMENT                          (Superpowers: subagent-driven-development where task warrants it)
→ LOCAL VERIFY                       (see below — distinguish pre-existing failures from regressions)
                                     [log phase]
→ REQUEST REVIEW                     (Superpowers: requesting-code-review, or implementation-reviewer agent)
→ HAND OFF TO PR                     (Superpowers: finishing-a-development-branch)  [log phase]
```

**If `FIND READY TASKS` returns an empty set:** report it plainly — no task selected, list what's
blocking every `BLOCKED` task and what would unblock it. Do not select a `BLOCKED`, `VERIFIED`, or
`MERGED` task because nothing else is available, and do not fabricate a task that isn't in the
artifact tree.

## Reading context

`READ CONTEXT` does not mean pulling the requirement, design, ADRs, and acceptance criteria
directly into the driving loop's own context. Dispatch a read-only Agent to gather them and return
a condensed digest — the acceptance criteria, and only the design constraints/ADRs actually
relevant to this task — rather than holding the full source documents in the loop that also has to
carry TDD/implementation/verify state for however long this task takes. Re-dispatch for a fuller
re-read if the digest turns out to be missing something the later steps need; don't silently guess
past a gap in it.

## Progress log and resuming

Every phase boundary marked `[log phase]` above gets one line appended to the task's own
`## Progress Log` section (`artifacts/task.md` template) — timestamp, phase, one-line detail. This
is the loop's external memory: if the agent's context is lost or compacted mid-task, the next
invocation must not restart blind or silently redo completed work.

**`CHECK PROGRESS LOG` runs right after task selection, before anything else:**

- **No log, or log shows no phases started:** fresh start, run the full workflow.
- **Log shows phases completed:** this is a resume. Do not redo those phases — but do not trust
  the log blindly either. Re-verify the claimed state before continuing (the branch exists and
  matches the logged commit, claimed-passing tests still pass). If reality doesn't match the log's
  claim, treat it as `IMPLEMENTATION_ERROR` and fall into the diagnose/retry path (see Failure
  handling below) rather than silently overwriting the discrepancy or trusting the stale claim.
- **`CHECK STALENESS` always re-runs on resume**, regardless of which phase the log says was last
  completed. A resumed task is exactly the case where time has passed and an upstream
  requirement/design could have been superseded since the log was last written — skipping the
  recheck because "we already got past that phase" defeats the point of the check.

## Task selection algorithm

Not the oldest or first issue. Evaluate ready tasks on readiness, dependency satisfaction,
priority, value, blocking potential, risk, size, critical-path relevance. Prefer smaller tasks
when value and dependencies are comparable. Conceptually:

```
score = value + blocking_value + readiness + critical_path_weight - risk_penalty - size_penalty
```

Doesn't need to be mathematically precise in v1 — make the policy explicit and let the human
override the pick at any time.

**Ceiling check, before scoring runs:** exclude any candidate whose `size` exceeds
`project.yaml`'s `task_sizing_policy.autonomous_ceiling` (default `L` — `XL` is never eligible,
full stop) from the candidate pool entirely. This is a hard filter, not a soft penalty term — a
mis-sized task that would otherwise score highest must not slip through via the formula. Route an
excluded task back to `plan` for decomposition; do not silently shrink its recorded size to make
it eligible.

**Deterministic tie-break:** if two or more candidates score identically after the ceiling check,
select the lowest task ID (creation order). Never resolve a tie randomly — the same ready-task set
must always produce the same pick.

## Staleness

Stale means: the task's `implements:`/`design:` field resolves to a requirement or design version
that is no longer the current `APPROVED` one — a supersession happened after this task was
planned. On detection, halt before implementing — do not build against the plan's original
assumptions. Re-run `plan` for this task against the current version (it may need re-scoping,
re-sizing, or splitting), or, only if the new version is confirmed not to affect this task's
scope, explicitly note that and proceed. Never assume "probably still fine" without checking.

## TDD policy

For application changes: RED (failing test) → GREEN (minimal implementation) → REFACTOR →
regression verification. Do not skip TDD silently. Where TDD doesn't apply (docs-only, static
config, pure design artifacts), the task must document why and what verification is used instead.
Writing tests after implementation and calling it TDD is not acceptable.

**Baseline first:** before writing this task's own RED test, capture which tests in the suite are
already failing — pre-existing, unrelated breakage is not this task's problem to fix. `LOCAL
VERIFY` must then separate two things: tests still red because of a pre-existing failure (report
it, don't silently inherit it, don't expand scope to fix it) versus tests newly red because this
change introduced a regression (block on this — never proceed with a self-caused regression).

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
- Resume a task by trusting its progress log without re-verifying the claimed state against reality
- Skip `CHECK STALENESS` on a resumed task because a prior phase already passed it
