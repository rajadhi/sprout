# Scenario: task planned against a requirement version that's since been superseded

**Tests:** `skills/develop-next/SKILL.md` — `CHECK STALENESS` step.
**Failure mode being prevented:** a task's `implements:` field points at a requirement ID that
has since gained a new version; an inadequate `develop-next` implements against the plan's
original (now-stale) assumptions instead of noticing the upstream requirement changed underneath
it.

## Input

Hypothetical: suppose `TASK-005` (generate draft from photo+calendar) had been planned and marked
`READY` back when `REQ-001` was still `v1` — which included location as an in-scope signal.
`develop-next` picks it up *after* the `v1 → v2` supersession (dropping location) has already
happened.

## Correct behavior

- `CHECK STALENESS` must detect that `TASK-005`'s `implements: [REQ-001]` now resolves to a
  different, non-equivalent version than what the task's `Purpose`/`Verification plan` assumed.
- Do not implement against the stale plan's assumptions (would build location-referencing code
  that `AC-001-04` in v2 explicitly forbids).
- Halt and route back — either re-run `plan` for this task against `REQ-001-v2`, or (if the task
  content is unaffected — this one wouldn't be, since v2 dropped a whole signal) confirm no
  changes needed and proceed.

## Walkthrough against current skill

The workflow has `CHECK STALENESS` as an explicit step between reading context and creating a
worktree — but the skill doesn't say what "stale" means precisely or what to do when it's
detected: does it block, or does it note the drift and proceed anyway?

**Gap found.** Fixed: defined staleness concretely (task's referenced requirement/design version
no longer matches the current `APPROVED` version) and made the halt-and-route behavior explicit.

## Verdict

**RED → GREEN.** See `skills/develop-next/SKILL.md` — `CHECK STALENESS` step now defines what
stale means and what happens when it's detected.
