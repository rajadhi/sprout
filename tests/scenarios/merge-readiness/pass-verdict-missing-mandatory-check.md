# Scenario: run verdict is PASS but never covered a mandatory check

**Tests:** `skills/merge-readiness/SKILL.md` — step 3, mandatory-check coverage.
**Failure mode being prevented:** this is the exact real-world case the original external review
caught in this repo's own ambient-journal dogfood example — `TASK-003` requires unit and
integration checks per its acceptance criteria, `project.yaml` policy also mandates `lint`, but
the recorded run only executed unit tests and still returned `PASS`, and the task was left at
`READY` rather than blocked. This scenario checks whether `merge-readiness` would have caught it
before merge, not just whether the gap was noticed after the fact.

## Input

`TASK-021` status `VERIFIED`. `RUN-00099` verdict `PASS`, `checks: [unit]`, `commit` matches the
PR head exactly. `artifacts/project.yaml`'s `verification_policy.mandatory_checks` is
`[lint, unit]`. The PR body reads "Task: TASK-021, all checks green."

## Correct behavior

- A `PASS` verdict on a run that never executed `lint` does not satisfy the project's mandatory
  checks — `merge_ready: false`, reason naming the specific missing check (`lint`) and that the
  run's own verdict field is not sufficient proof by itself.
- Must not be swayed by the PR description's confident framing ("all checks green") — that's the
  PR author's claim, not evidence; the skill resolves the run's actual `checks:` list against
  policy rather than trusting prose in the description.

## Walkthrough against current skill

Step 3's second bullet explicitly says a run's `checks:` list must be a superset of
`verification_policy.mandatory_checks`, and states plainly: "A run missing a mandatory check
fails, even with verdict PASS." Step 6 forbids softening a fail because "the surrounding work
looks well-intentioned" — directly on point for the PR body's confident-but-unverified claim.

**Gap check:** none found — step 3 as written already produces `merge_ready: false` here.

## Verdict

**GREEN.** Confirms the mandatory-check-coverage rule discriminates a real case this project
already got wrong once, not just a hypothetical.
