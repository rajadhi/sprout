# Scenario: GitHub issue closed but the local task never reached VERIFIED

**Tests:** `skills/doctor/SKILL.md` — check 7, closed-issue drift.
**Failure mode being prevented:** `doctor` picking a side on an ambiguous case it has no way to
actually resolve — either silently ignoring a closed issue on the assumption "closed means done,
nothing to report," or confidently asserting the task must have been abandoned and suggesting the
task file itself be edited to `RETIRED`. Both are unearned certainty from a check that can only
observe a disagreement, not its cause.

## Input

`TASK-051.md`: `status: IMPLEMENTING`, `github_issue: 77`. `gh issue list` for issue 77 returns
`state: closed`, no `retirement_reason` anywhere in `TASK-051.md`.

## Correct behavior

- `doctor` reports this as drift — closed issue, task not at or past `VERIFIED` — per check 7's
  third bullet.
- The finding does not assert which side is wrong. It states the disagreement (issue closed,
  task still `IMPLEMENTING`) and lets a human decide whether the issue was closed prematurely
  (patch: reopen it) or the task was actually abandoned and never got a proper `RETIRED`
  transition (a decision for a human via `plan`/`graph`, not something check 7 invents on its
  own).
- No patch command is offered that resolves the ambiguity one way — at most, a patch to bring the
  issue's *state* back to matching what the task's current (unresolved) status implies (reopened),
  offered as one option, not a definitive fix.

## Walkthrough against current skill

Check 7's third bullet describes exactly this case and explicitly declines to pick a side:
"`doctor` can't tell which, so it reports both as equally plausible rather than picking one." This
is consistent with the skill's overall Overview ("most fixes here are judgment calls... not
mechanical") and the pre-existing Must-not ("Auto-fix a finding without human judgment").

**Gap check:** none found — the skill already generalizes its no-auto-fix, report-don't-resolve
posture to this new check without needing separate special-casing.

## Verdict

**GREEN.** The ambiguous case is handled the same principled way doctor already handles every
other judgment-call finding — reported, not resolved — rather than needing new logic bolted on
for GitHub-specific drift.
