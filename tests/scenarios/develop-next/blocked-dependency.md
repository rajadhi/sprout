# Scenario: blocked dependency

**Tests:** `skills/develop-next/SKILL.md` — `FIND READY TASKS` step.
**Failure mode being prevented:** a task whose status is `BLOCKED` gets selected anyway because
its score would otherwise be high (small, low-risk).

## Input

`TASK-009` from the Ambient Journal fixture — `status: BLOCKED`, waiting on `DES-001-v2`. It's
`XS`/`R1`, which would score well if size/risk were the only inputs.

## Correct behavior

- `TASK-009` is excluded from the ready-task pool entirely — `FIND READY TASKS` filters on
  `status: READY`, and `BLOCKED` doesn't qualify regardless of how favorably it would otherwise
  score.
- If `TASK-009` were the only task with work available, this collapses into the `no-ready-tasks`
  scenario, not "select it anyway since nothing else is available."

## Walkthrough against current skill

`FIND READY TASKS` is a distinct step before `SELECT ONE TASK` — a `BLOCKED` task never enters the
candidate pool the selection formula runs against, so there's no path for it to be picked by
scoring alone.

**Gap check:** none found. The status filter, taken literally, already excludes this case; the
`no-ready-tasks` fix (empty-set handling) covers the fallback correctly.

## Verdict

**PASS**, no additional skill change needed beyond the `no-ready-tasks` fix.
