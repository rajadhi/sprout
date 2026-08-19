# Scenario: no ready tasks

**Tests:** `skills/develop-next/SKILL.md` — `FIND READY TASKS` step.
**Failure mode being prevented:** an inadequate `develop-next` picks a `BLOCKED` or `VERIFIED`
task anyway because "some task has to be selected," or silently fabricates a plausible-sounding
task instead of reporting the true state.

## Input

Project state where every task is `BLOCKED`, `VERIFIED`, or `MERGED` — no task in `READY`. (Not
hypothetical: after `TASK-001`–`TASK-008` in the Ambient Journal fixture reach `VERIFIED`/`MERGED`
and `TASK-009` stays `BLOCKED` on `DES-001-v2`, this is exactly the state.)

## Correct behavior

- Report plainly: no ready tasks, name what's blocking the blocked ones (`TASK-009` needs
  `DES-001-v2`).
- Do not select `TASK-009` anyway "since it's the only one left."
- Do not invent a task that isn't in the artifact tree.
- Suggest the actual unblock path: run `design` again to produce `DES-001-v2`.

## Walkthrough against current skill

Workflow step 2 is `FIND READY TASKS`, before `SELECT ONE TASK` — if that set is empty, there's
nothing for step 3 to select from. The skill doesn't currently say what to do when the set is
empty.

**Gap found.** Fixed: added an explicit empty-set behavior.

## Verdict

**RED → GREEN.** See `skills/develop-next/SKILL.md` — workflow now states the empty-`READY`-set
case explicitly.
