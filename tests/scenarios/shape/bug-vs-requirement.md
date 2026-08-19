# Scenario: bug reported as if it were a new requirement

**Tests:** `skills/shape/SKILL.md` — `Bug` classification rule.
**Failure mode being prevented:** an inadequate `shape` creates `REQ-XXX v(N+1)` for something
that is actually a defective implementation of the existing, still-correct requirement — inflating
requirement history with noise and hiding the real problem (a code bug) behind a spec change.

## Input

Existing approved requirement `REQ-014 v1`: *"Saving an entry persists it immediately; reopening
the app shows the saved entry."*

New raw intent: *"When I save an entry and force-quit the app right after, the entry is gone when
I reopen it."*

## Correct behavior

- Classify as `BUG`, not `NEW`/`REFINEMENT`/`SUPERSESSION`.
- `REQ-014` is still correct as written — the desired behavior (persist immediately, survive
  reopen) hasn't changed. What's wrong is the implementation not actually persisting before
  force-quit.
- Do not create `REQ-014 v2`.
- Route to `develop-next`'s diagnose path (`IMPLEMENTATION_ERROR` classification) instead of the
  shape → design → plan pipeline.

## Walkthrough against current skill

Classification rules: *"Bug — the requirement remains correct; the implementation is wrong. Do
not create a new product requirement merely because code is defective — route to develop-next's
diagnose path instead."* Directly matches. The `CLASSIFY` step happens before
`GENERATE REQUIREMENTS`, so a correctly-classified bug never reaches requirement-generation at
all.

**Gap check:** the routing target — "develop-next's diagnose path" — exists as
`skills/develop-next/SKILL.md`'s failure-handling section, and covers exactly this via
`IMPLEMENTATION_ERROR` classification. Consistent.

## Verdict

**PASS**, no skill change needed.
