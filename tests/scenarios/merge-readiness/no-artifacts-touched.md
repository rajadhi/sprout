# Scenario: ordinary code/docs PR touches no Sprout artifacts at all

**Tests:** `skills/merge-readiness/SKILL.md` — step 1, scope boundary.
**Failure mode being prevented:** the opposite failure from the other scenarios in this directory
— this check becoming a blanket gate that fails every PR in the repo (a typo fix, a README edit, a
CI workflow tweak) because it can't find a task to resolve. That would make the check something
teams disable rather than trust, which defeats the purpose as surely as not enforcing anything at
all.

## Input

A PR that fixes a broken link in `README.md`. It touches no `TASK-*.md`, `RUN-*.md`, `EVD-*.md`,
or `APR-*.md` file, and its description names no task ID.

## Correct behavior

- `merge_ready: true`, reason stating plainly that there was nothing to verify — not a fabricated
  task reference, and not a fail for "no task associated."

## Walkthrough against current skill

Step 1 handles this directly: "If the diff touches no `TASK-*.md`/`RUN-*.md`/`EVD-*.md`/
`APR-*.md` files and the PR description names no task, there is nothing to check ... record
`merge_ready: true` ... and stop." The Must-not list separately forbids blocking a PR that touches
no Sprout artifacts, naming it as scope creep past `merge_policy`.

**Gap check:** none found.

## Verdict

**GREEN.** Confirms the check has an explicit, deliberate floor and won't degrade into a
repo-wide obstacle for unrelated changes.
