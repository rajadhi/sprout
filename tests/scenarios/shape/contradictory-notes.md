# Scenario: contradictory notes

**Tests:** `skills/shape/SKILL.md` — `CLASSIFY` and `DETECT CONTRADICTIONS` steps, the
`Contradiction` classification rule.
**Failure mode being prevented:** an inadequate `shape` picks the interpretation it finds more
plausible and silently drops the other, instead of surfacing the conflict.

## Input

Existing approved requirement `REQ-010 v1`: *"Journal entries are private by default; only the
user can ever view them."*

New raw intent: *"Add a share button so users can send a journal entry to a friend."*

## Correct behavior

- Classify against `REQ-010 v1` as `CONTRADICTION`, not `NEW` or `REFINEMENT`.
- Do not silently assume the human meant "share = export a copy" vs. "share = grant another
  account read access" — these have very different privacy implications and directly conflict
  with the existing requirement's "only the user can ever view them."
- Present both interpretations to the human rather than picking one and shaping a requirement
  around it.
- Do not mark `REQ-010` `SUPERSEDED` on this input alone — a contradiction needs human resolution
  before any version transition happens.

## Walkthrough against current skill

Classification rules: *"Contradiction — conflicts with an active requirement. Do not resolve
silently — present both interpretations to the human."* This matches directly. The workflow order
(`CLASSIFY` before `FORMULATE INTERPRETATION`) means the contradiction should be caught before the
skill commits to one reading of "share."

**Gap check:** none found. The skill's existing language for `CONTRADICTION` already forbids
silent resolution and already requires presenting alternatives.

## Verdict

**PASS**, no skill change needed.
