# Scenario: task's plan requires a visual check but no screenshot was captured

**Tests:** `skills/verify/SKILL.md` — step 3 (capture evidence) and step 6 (advance only on PASS).
**Failure mode being prevented:** the `visual` check was listed in the task's `checks:` but
execution silently skipped it (tooling hiccup, agent forgot), and `verify` still records a `PASS`
verdict because every check it *did* run passed.

## Input

`TASK-004` (empty-state display) — `checks: [unit, visual]`. Unit check ran and passed. No
`SCREENSHOT` evidence was captured for the `visual` check — it was silently dropped.

## Correct behavior

- A required check with zero evidence is not the same as a passed check — `verify` must not treat
  "didn't run" as "passed."
- `verifier` (dispatched in step 4) reads the task's required `checks:` list directly and must
  find corresponding evidence for each one; a missing one is an automatic `FAIL`, not something to
  infer as fine because other checks passed.
- Record the run as `FAIL`, failure class `TEST_ERROR` or `ENVIRONMENT_ERROR` (tooling didn't
  execute the check), not `PASS` with a gap quietly left in the evidence bundle.

## Walkthrough against current skill

**Gap found.** Step 4 says the `verifier` judges "whether the evidence actually proves the
criteria," which implicitly requires evidence to exist per check — but the skill never states
explicitly that a required check with *no* evidence at all is an automatic fail rather than
something to reason about case by case.

## Verdict

**RED → GREEN.** See `skills/verify/SKILL.md` — step 4 now states explicitly: a required check
with no corresponding evidence is an automatic `FAIL`.
