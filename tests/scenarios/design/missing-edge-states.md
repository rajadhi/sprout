# Scenario: design covers only the happy path

**Tests:** `skills/design/SKILL.md` — `REVIEW EDGE STATES` step, `ux-critic`'s edge-state check.
**Failure mode being prevented:** a design candidate that looks polished for the happy path but
never specifies what the empty/loading/error states look like, leaving them as implicit
afterthoughts an implementer has to invent later — outside review.

## Input

Requirement: "Display the user's journal entries for the current day." Draft design candidate
covers only the case where entries already exist — a populated list, nicely laid out.

## Correct behavior

- `ux-critic` must flag the missing empty state (first day, no entries yet — what does the user
  see?), loading state (entries fetching), and error state (fetch failed) as findings, not pass
  the design through.
- The design is not presented for approval until all three are specified in `artifacts/design.md`
  under their dedicated sections.

## Walkthrough against current skill

`design`'s workflow has an explicit `REVIEW EDGE STATES (empty, loading, error)` step, and "Must
not" already says *"Skip edge states... because they're less visually interesting."*
`artifacts/design.md` has dedicated `### Empty state` / `### Loading state` / `### Error state`
sections — an incomplete design candidate would ship the template with those sections blank,
which is visible and checkable.

**Gap check:** `ux-critic`'s own checklist has "Edge-state coverage" listed, but doesn't say what
to do when it's blank vs. thin — should a one-line "TBD" pass? Fixed: clarified that blank or
placeholder edge-state sections are themselves a finding, not just structurally-absent ones.

## Verdict

**RED → GREEN.** See `agents/ux-critic.md` — clarified blank/placeholder edge states count as
findings.
