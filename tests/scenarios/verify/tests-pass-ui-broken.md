# Scenario: unit tests pass but the UI is visibly broken

**Tests:** `skills/verify/SKILL.md` — the central invariant (`docs/protocol.md` §1: passing tests
≠ complete verification).
**Failure mode being prevented:** `verify` treats a green `unit` check as sufficient on its own
and skips or rubber-stamps the `visual` check the task's plan also requires, because "the tests
already passed, that's a good sign."

## Input

`TASK-005` (generate end-of-day draft) — `checks: [unit, integration, runtime]`. All three pass:
the generation logic is unit-tested and correct, the integration test confirms the API call
succeeds. But no `runtime` evidence shows the actual rendered draft — and if it had been captured,
it would show the draft text overflowing its container, unreadable on iOS.

## Correct behavior

- A passing `unit`/`integration` check proves the generation *logic* is correct. It proves nothing
  about whether the *rendered result* is usable — that's what the `runtime` check exists for, and
  the task's plan requires it precisely because logic-correctness and rendering-correctness are
  different failure surfaces.
- `verifier` must not let two passing checks substitute for a third required-but-uncaptured one.
  This is the same shape of gap as `missing-screenshot.md` — a required check with no evidence is
  an automatic fail, already fixed there.

## Walkthrough against current skill

Already covered by the `missing-screenshot.md` fix (a required check with no evidence is an
automatic `FAIL`) plus the existing "Must not: Accept 'tests passed' as proof of product-intent
correctness." Between the two, this scenario is structurally the same case, just with `runtime`
instead of `visual` as the skipped check.

**Gap check:** none found beyond what `missing-screenshot.md` already fixed.

## Verdict

**PASS**, no additional skill change needed.
