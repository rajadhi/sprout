# Scenario: design presented for approval with an unresolved critic finding

**Tests:** `skills/design/SKILL.md` — the "Approval gate" section's precision.
**Failure mode being prevented:** the workflow runs `CRITIQUE USABILITY → REVISE → RE-EVALUATE`
once, `ux-critic` reports a real finding (e.g. requirement says "user can undo a delete within 5
seconds," design has no undo affordance at all), but the skill presents the design for approval
anyway because "design quality gate passes" is vague enough to not obviously mean "both critics
now report zero open findings."

## Input

`ux-critic` finding: *"Delete flow: no undo affordance. REQ-031 AC-031-02 requires undo within 5
seconds of delete — design has no path back."* Design presented for human approval regardless.

## Correct behavior

- A design must not reach the human for approval while any critic finding is still open.
- "Design quality gate passes" must mean, concretely: `ux-critic` and `accessibility-critic` both
  report zero findings on the current candidate — not just that a critique pass happened once.

## Walkthrough against current skill

The workflow shows `CRITIQUE → REVIEW EDGE STATES → REVISE → RE-EVALUATE → PRESENT`, implying a
loop back on findings, but the "Approval gate" section's phrase "design quality gate passes" never
actually defines what that means in checkable terms — a literal reading could treat "ran the
critique step" as sufficient even with open findings.

**Gap check:** real gap. Fixed by making the approval gate condition explicit and unambiguous.

## Verdict

**RED → GREEN.** See `skills/design/SKILL.md` — "Approval gate" now spells out the pass
condition instead of the vague "design quality gate passes."
