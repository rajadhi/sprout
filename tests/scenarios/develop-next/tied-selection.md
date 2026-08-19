# Scenario: multiple equally eligible tasks

**Tests:** `skills/develop-next/SKILL.md` — task selection algorithm.
**Failure mode being prevented:** two tasks score identically and an inadequate `develop-next`
picks one arbitrarily/randomly each run, making task order non-reproducible and hard to reason
about across sessions.

## Input

`TASK-001` (photo consent) and `TASK-002` (calendar consent) from the Ambient Journal fixture:
same size (S), same risk (R1), same dependency count (zero), both `READY`, neither blocking the
other. The selection formula `score = value + blocking_value + readiness + critical_path_weight -
risk_penalty - size_penalty` produces the same number for both.

## Correct behavior

- The tie must resolve deterministically, not randomly — same inputs, same pick, every time.
- Reasonable deterministic tie-break: lower task ID first (creation order), since neither task
  has a stronger claim on any other dimension.

## Walkthrough against current skill

**Gap found.** The selection algorithm section describes the scoring formula and says "prefer
smaller tasks when value and dependencies are comparable," but doesn't say what happens when
*everything* is comparable, including size. No tie-break rule existed.

## Verdict

**RED → GREEN.** See `skills/develop-next/SKILL.md` — added explicit deterministic tie-break
(lowest task ID) to the selection algorithm section.
