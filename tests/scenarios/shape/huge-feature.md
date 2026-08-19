# Scenario: huge feature bundling unrelated outcomes

**Tests:** `skills/shape/SKILL.md` — `GENERATE REQUIREMENTS` step.
**Failure mode being prevented:** an inadequate `shape` produces one omnibus requirement covering
several unrelated outcomes, which a human then can't meaningfully approve or reject as a unit —
they'd have to accept or block all of it together.

## Input

> "I want a redesign: new onboarding flow, dark mode, in-app search, and a way to share entries
> with friends."

## Correct behavior

- Recognize these as four independent outcomes with no shared problem statement — onboarding,
  theming, search, and sharing don't share acceptance criteria or fail/succeed together.
- Produce four separate requirement candidates (`REQ-XXX` through `REQ-(XXX+3)`), each independently
  approvable/rejectable, rather than one requirement with four unrelated sub-sections.
- This is a requirement-level analogue of the task-sizing invariant (`docs/protocol.md` §1.5) —
  small, independently reviewable units, applied one level up from tasks.
- Sharing in particular should also run through contradiction detection against any existing
  privacy-related requirement (see `contradictory-notes.md`).

## Walkthrough against current skill

**Gap found.** The workflow's `GENERATE REQUIREMENTS` step is plural in name but nothing in the
skill instructs splitting a bundled ask into independent requirement candidates — a literal
reading could produce one requirement with sprawling scope. Fixed: added an explicit rule.

## Verdict

**RED → GREEN.** See `skills/shape/SKILL.md` — new "Requirement granularity" section added.
