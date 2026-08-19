# Scenario: evidence was captured against the wrong commit

**Tests:** `skills/verify/SKILL.md` / `artifacts/verification-run.md` — commit/environment
identity.
**Failure mode being prevented:** the branch got a late fixup commit after evidence was already
captured, but `verify` records the run against the branch name rather than the exact commit SHA —
so the "verified" evidence doesn't actually correspond to what eventually merges.

## Input

`TASK-003` branch: evidence captured at commit `abc123`. A small fixup commit `def456` lands after
(e.g. addressing an `implementation-reviewer` finding) but `verify` is not re-run — the existing
`RUN-XXXXXX` for `abc123` is treated as still valid for `def456`.

## Correct behavior

- `artifacts/verification-run.md`'s `commit` field is the exact SHA the evidence was captured
  against. A run for `abc123` proves nothing about `def456` — any commit after the verified one
  requires its own run, however small the diff looks.
- Do not let "the fixup was trivial" become an implicit exemption — `docs/protocol.md` §1's
  central rule (advance state only when evidence/policy conditions are satisfied, not agent
  judgment) applies exactly here: an agent deciding a fixup is "trivial enough to skip
  re-verification" is exactly the kind of unearned advancement the rule exists to block.

## Walkthrough against current skill

`artifacts/verification-run.md`'s schema already has a `commit` field, and the docstring says "a
later run against the same task creates the next `RUN-XXXXXX`" — but the skill/template don't
explicitly forbid treating a run for commit A as covering a later commit B on the same branch.

**Gap found.** Fixed by making the commit-identity requirement explicit rather than implied by
the schema field's mere existence.

## Verdict

**RED → GREEN.** See `skills/verify/SKILL.md` — step 5 now states explicitly that any commit
after the verified one, however small the diff, needs its own run.
