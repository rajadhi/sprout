# Scenario: color-only status signaling

**Tests:** `agents/accessibility-critic.md` — "no color-only signaling" check.
**Failure mode being prevented:** a visually clean design that signals state (e.g. "entry saved"
vs. "save failed") through color alone, which is invisible to colorblind users and anyone not
looking directly at the indicator when it changes.

## Input

Design candidate for a save-status indicator: a small dot that turns green on success, red on
failure. No text, icon, or shape change between states.

## Correct behavior

- `accessibility-critic` flags this as a finding: color is the only differentiator between two
  states that matter (success vs. failure).
- Fix direction: pair color with an icon (check vs. exclamation) or text label, not just note the
  problem and move on.
- Design does not pass the accessibility gate until fixed.

## Walkthrough against current skill

`accessibility-critic`'s web checklist explicitly lists "no color-only signaling" under the WCAG
2.2 AA check set. This input is exactly that failure mode — directly covered.

**Gap check:** none found. The existing checklist item is specific enough to catch this without
modification.

## Verdict

**PASS**, no agent change needed.
