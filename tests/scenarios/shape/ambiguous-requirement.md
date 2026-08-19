# Scenario: ambiguous requirement

**Tests:** `skills/shape/SKILL.md` — the "acceptance criteria bar" and "identify unknowns" steps.
**Failure mode being prevented:** an inadequate `shape` invents a plausible-sounding acceptance
criterion instead of admitting the input doesn't support one yet.

## Input

> "Users should be able to search their notes easily."

## Correct behavior

- Classify as `NEW`.
- Flag `"easily"` as non-testable — do not silently translate it into an invented concrete
  criterion (e.g. do not invent "results appear in under 200ms" out of nothing).
- Record it as an unknown: what does "easily" mean here — result relevance, speed, discoverability
  of the search entry point? Ask, don't guess.
- Do not advance to `READY_FOR_REVIEW` with only vague criteria; either the human resolves the
  unknown or the requirement stays in `SHAPING`.

## Walkthrough against current skill

`shape`'s "Acceptance criteria bar" section: *"Reject criteria like 'the experience should feel
intuitive' unless paired with a concrete, observable assertion."* — the same class of vagueness as
"easily." The workflow's `IDENTIFY UNKNOWNS` step runs before `GENERATE ACCEPTANCE CRITERIA`, so
an unresolved unknown here should block criteria generation rather than get papered over.

**Gap check:** the skill doesn't explicitly say what happens when *every* candidate acceptance
criterion for a requirement is unresolvable — does the requirement still reach
`READY_FOR_REVIEW` with zero criteria? `artifacts/requirement.md` already requires at least one
AC "except where explicitly classified as a non-functional constraint" — this input isn't that,
so the requirement must stay in `SHAPING` with the unknown surfaced, not be presented for approval
prematurely.

## Verdict

**RED → GREEN.** Gap found: the skill didn't explicitly forbid advancing a requirement to
`READY_FOR_REVIEW` when every acceptance criterion is unresolvably vague. Fixed in
`skills/shape/SKILL.md` — "Acceptance criteria bar" now states this explicitly: stay in
`SHAPING`, record the vagueness under Unknowns, surface as an open question. **PASS** after fix.
