# Scenario: implementation diverges from an already-approved accessible design

**Tests:** `skills/verify/SKILL.md` interaction with `agents/verifier.md` — verification
independence.
**Failure mode being prevented:** `DES-001` was already approved with `accessibility-critic`
finding zero open issues (see the M2 fixture). But the *implementation* of `TASK-001`'s consent
prompt doesn't actually match what was approved — VoiceOver reads it as generic "Allow Photos
Access" instead of the specific purpose text `DES-001`'s Copy rules require. Design review already
happened and passed; this is an implementation regression against an approved spec, not a design
gap.

## Input

`TASK-001` evidence includes an `ACCESSIBILITY_REPORT` showing the consent prompt's VoiceOver
label as generic "Allow Photos Access," contradicting `DES-001`'s Copy rules section.

## Correct behavior

- `verifier` must catch this even though the *design* already passed accessibility review — the
  check here is implementation-vs-approved-design fidelity, a different failure surface than
  design-quality review, and it's `verify`'s job (via the `review`/`accessibility`-relevant
  evidence), not something to assume is already covered because `DES-001` was clean.
- Record `FAIL`, failure class `ACCESSIBILITY_ERROR` (implementation diverged from spec, not a
  spec defect — the spec was already right).

## Walkthrough against current skill

`verifier`'s own steps say to read the requirement/acceptance criteria directly — but
`artifacts/task.md`'s `design:` reference means the verifier's evidence-sufficiency judgment
should also be checked against the approved design's specifics (Copy rules, accessibility
section), not only the abstract acceptance criteria text.

**Gap found.** `agents/verifier.md`'s steps don't mention checking implementation evidence against
the *design* artifact's specifics when a task has one, only against requirement acceptance
criteria.

## Verdict

**RED → GREEN.** See `agents/verifier.md` — step 1 now includes reading the referenced design
artifact's specifics (not just the requirement) when the task has a `design:` reference.
