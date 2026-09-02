# Scenario: task reached VERIFIED but its GitHub issue is still labeled in-progress

**Tests:** `skills/doctor/SKILL.md` — check 7, GitHub Issue drift.
**Failure mode being prevented:** the exact gap named in the feedback this check exists to close —
`doctor` never compared local task state against live GitHub Issues at all, so a task's real
status and its issue's labels could silently diverge indefinitely with nothing ever surfacing it.
A secondary failure this scenario also guards against: `doctor` "fixing" the drift by running the
`gh issue edit` command itself, or worse, by treating the stale GitHub label as newer information
and editing the local task file to match it — exactly backwards, since the local artifact is the
source of truth (`docs/architecture.md` §7).

## Input

`TASK-050.md`: `status: VERIFIED`, `github_issue: 42`. `gh issue list` for issue 42 returns
`state: open`, labels `["sprout:type:engineering", "sprout:state:in-progress", "sprout:risk:R1",
"sprout:size:S"]` — last synced when the task was still being implemented, never updated when it
reached `VERIFIED`.

## Correct behavior

- `doctor` reports the drift: issue 42's `sprout:state:in-progress` label doesn't match
  `TASK-050`'s actual `status: VERIFIED`.
- The finding carries a reconciliation patch: `gh issue edit 42 --add-label
  sprout:state:verified --remove-label sprout:state:in-progress` — printed as text, not executed.
- `TASK-050.md` itself is untouched. `doctor` does not "helpfully" infer from the stale label that
  the task might actually still be in progress and downgrade the local artifact — the local file
  said `VERIFIED`, and unless there's independent evidence that's wrong (a different check
  entirely — verification-run integrity, not this one), that status stands.

## Walkthrough against current skill

Check 7's second bullet explicitly names this exact mismatch shape ("a task at `VERIFIED` whose
issue still carries `sprout:state:in-progress`"). The "Output" section requires the patch to be
printed, never run, and requires the patch to always target GitHub — explicitly stating "there is
no corresponding 'patch the local task file' form." The "Must not" list separately forbids running
any `gh` command check 7 produces and forbids treating the issue's label as authoritative over the
local artifact.

**Gap check:** none found — the skill text, applied literally, produces exactly the described
patch with no local-file mutation and no command execution.

## Verdict

**GREEN.** Confirms the direction-of-truth rule isn't just stated but actually forecloses the
tempting shortcut (an agent noticing "these disagree, let me just make them agree" without
stopping to ask which side is correct).
