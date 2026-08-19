# Scenario: pre-existing test failures unrelated to this task

**Tests:** `skills/develop-next/SKILL.md` — TDD policy, `LOCAL VERIFY` step.
**Failure mode being prevented:** the repo already has unrelated failing tests before this task's
branch starts. An inadequate `develop-next` either (a) treats every red test as caused by its own
change and burns effort "fixing" pre-existing breakage out of scope, or (b) treats "some tests are
red" as fine because the baseline was already red, masking a regression its own change introduced
among the noise.

## Input

`TASK-007` (inline edit persists) branch created. Before writing `TASK-007`'s own RED test, the
existing suite already has 2 unrelated failing tests (e.g. a flaky calendar-fetch integration test
from `TASK-005`'s scope, not this task's).

## Correct behavior

- Record the baseline failure state *before* starting TDD for this task — which tests are red
  going in.
- `TASK-007`'s own RED → GREEN cycle is scoped to the test(s) it adds/modifies. Don't touch the
  2 pre-existing failures as part of this task — that's scope creep into someone else's task.
- `LOCAL VERIFY` must distinguish "still red because of pre-existing unrelated failure" (acceptable
  to proceed, but must be reported, not hidden) from "red because this change introduced a
  regression" (must not proceed).
- Report the pre-existing failures in the PR/evidence so they're visible, not silently inherited.

## Walkthrough against current skill

**Gap found.** The workflow doesn't mention capturing a baseline before starting TDD, and
`LOCAL VERIFY` doesn't distinguish pre-existing failures from newly introduced ones — a literal
reading of "RED → GREEN → REFACTOR → regression verification" could be satisfied by "the tests I
personally touched are green" while ignoring whether the overall suite got worse.

## Verdict

**RED → GREEN.** See `skills/develop-next/SKILL.md` — TDD policy now requires capturing a
baseline before starting, and `LOCAL VERIFY` must separate pre-existing failures (reported, not
fixed in scope) from newly introduced regressions (block on).
