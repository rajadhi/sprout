# Scenario: API check captures only the status code

**Tests:** `skills/verify/SKILL.md` — "Evidence sufficiency bar."
**Failure mode being prevented:** an `integration` check for an endpoint captures `HTTP 200` and
calls it done — exactly the insufficiency the skill already warns against, tested here for real
against a concrete input rather than trusting the warning gets followed.

## Input

`TASK-001` (photo consent). Its `integration` check hits the consent-storage endpoint after
granting consent. Captured evidence: `POST /consent {signal: photo} -> 200 OK`. Nothing else.

## Correct behavior

- `200 OK` alone does not prove AC-003-01/03 (consent actually stored, persists, purpose text was
  specific). The evidence must also include: response body showing the stored consent record,
  and — since this is persistence-relevant — a follow-up read confirming the write actually took
  effect, not just that the write endpoint returned success.
- `verifier` must reject this evidence as insufficient and record `FAIL` (or send it back for
  re-capture), not accept the status code as proof.

## Walkthrough against current skill

The "Evidence sufficiency bar" section already gives this exact example almost verbatim ("Not
sufficient: HTTP 200 alone... Sufficient: HTTP 200 + schema validation + required fields present +
expected persisted state"). Applying it directly: this evidence is missing the persisted-state
check, so it fails the bar as written.

**Gap check:** none found — the existing bar, applied literally, already produces the correct
verdict.

## Verdict

**PASS**, no skill change needed. (Confirms the sufficiency bar isn't just well-worded but
actually discriminates a real insufficient-evidence case.)
