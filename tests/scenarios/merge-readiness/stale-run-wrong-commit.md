# Scenario: verification run's commit predates the PR's actual head

**Tests:** `skills/merge-readiness/SKILL.md` — step 3, commit-SHA binding.
**Failure mode being prevented:** exactly the gap the original review named as the central
invariant failure — "the workflow never binds a PR's implementation to a ... current commit SHA.
A code-only PR can therefore pass Sprout's CI without participating in Sprout at all." A task was
verified once, then the branch picked up a real code fixup commit afterward (a rebase, a review
fixup, a merge of `main`) with no new verification run. `skills/verify/SKILL.md` step 5 already
says this needs its own run, but nothing checked that the rule was actually followed before merge
— this scenario tests whether `merge-readiness` catches it when it wasn't.

## Input

`TASK-014` (status `VERIFIED`) references `RUN-00042`, `verdict: PASS`, `checks: [lint, unit]`,
`commit: a1b2c3d`. The PR under review has head SHA `f9e8d7c` — three commits ahead of `a1b2c3d`,
including a genuine logic change made after the run (a review-requested fix to the exact code path
`RUN-00042` exercised). The PR description says "Task: TASK-014" and nothing else has changed
about the task or run.

## Correct behavior

- `RUN-00042`'s `commit` (`a1b2c3d`) is not the PR head (`f9e8d7c`) and is not treated as
  equivalent to it just because the task/run IDs match and the verdict reads `PASS`.
- `merge_ready: false`, with a reason naming the exact SHA mismatch — not a vague "verification
  looks stale."
- The fact that `TASK-014`'s frontmatter status still says `VERIFIED` must not be accepted at face
  value; the skill resolves the run's actual `commit` field rather than trusting the task's status
  as sufficient proof on its own.

## Walkthrough against current skill

Step 3 explicitly requires the run's `commit` to equal the PR head SHA or be an ancestor of it,
named as a hard fail condition ("A run captured against a different, earlier, or unrelated commit
does not prove *this* diff was verified"). Step 6 requires citing the specific field and value,
which forces the SHA mismatch to be named rather than summarized away.

**Gap check:** none found — applying step 3 literally to this input produces `merge_ready: false`
with the SHA named.

## Verdict

**GREEN.** The skill's commit-binding step, applied literally, catches this case.
