# Scenario: delegated context digest is missing something a later phase needs

**Tests:** `skills/develop-next/SKILL.md` — `READ CONTEXT` step, "Reading context".
**Failure mode being prevented:** `READ CONTEXT` delegates to a subagent that returns a condensed
digest instead of the full requirement/design/ADR set, to keep the driving loop's own context
from being spent holding source documents for the whole multi-phase task. An inadequate
`develop-next` either (a) reverts to habit and reads everything directly anyway, defeating the
point, or (b) trusts the digest as complete and, on hitting a gap during TDD/implementation,
silently guesses or proceeds without the missing constraint rather than noticing the digest was
incomplete and going back for it.

## Input

`TASK-014` (export draft as PDF) has `architecture: [ADR-003, ADR-007]`. The dispatched digest
subagent's summary covers `ADR-003` (export format decision) but omits `ADR-007` (a later decision
constraining PDF file naming, filed after the task was planned) — an incomplete digest, not a
malicious one. Partway through `IMPLEMENT`, the agent needs to decide a file-naming scheme and the
digest has nothing on it.

## Correct behavior

- `READ CONTEXT` uses the delegated digest, not a direct full read of every referenced document —
  the loop's own context stays spent on TDD/implementation/verify state, not on re-holding source
  docs.
- On hitting the file-naming decision with no coverage in the digest, `develop-next` must notice
  the gap rather than invent a naming scheme or silently skip the constraint. It re-dispatches
  (per "Reading context": *"Re-dispatch for a fuller re-read if the digest turns out to be missing
  something the later steps need; don't silently guess past a gap in it"*) specifically for
  `ADR-007`, gets the actual constraint, and implements against it.

## Walkthrough against skill before this change

Before this change, `READ FULL CONTEXT` meant reading every referenced document directly into the
loop — there was no digest step and therefore no gap-detection behavior to define, but also no
protection against the loop's context filling up with full source documents across a long-running
task. Once delegation was introduced to solve that, a literal reading of "dispatch an Agent for a
digest" without further guidance could be satisfied by an agent that treats the digest as
complete and never checks back — reintroducing exactly the "invented assumption filling a gap"
failure mode `specification-critic` exists to catch elsewhere in the framework, just relocated to
`develop-next`.

**Gap found.** Fixed: "Reading context" explicitly requires re-dispatching for a fuller read when
the digest is missing something a later step needs, and explicitly forbids silently guessing past
the gap.

## Verdict

**RED → GREEN.** See `skills/develop-next/SKILL.md` — "Reading context" section now requires
re-dispatch on a detected gap rather than silent invention or a full-read fallback out of habit.
