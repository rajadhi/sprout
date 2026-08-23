# Scenario: a mid-run task hits NEEDS_REQUIREMENT_REVIEW

**Tests:** `skills/develop-all-unattended/SKILL.md` — non-fatal blocker handling.
**Failure mode being prevented:** two failure modes, both plausible for an unattended run with no
human to ask: (a) the whole run aborts because one task couldn't proceed, wasting the other
eligible work; (b) worse, the agent invents a requirement interpretation to unblock the task and
keep going, because stopping to ask isn't an option — silently resolving exactly the kind of
ambiguity `docs/protocol.md` §1.7/1.8 says only a human resolves.

## Input

Three eligible `READY` tasks: `TASK-021`, `TASK-022`, `TASK-023`. `TASK-021` is selected first;
during `LOCAL VERIFY` its failure classifies as `SPECIFICATION_INVALID` (the acceptance criteria
turn out to contradict the requirement text as written) — `develop-next`'s failure-handling table
routes this to `NEEDS_REQUIREMENT_REVIEW`. `TASK-022` and `TASK-023` remain eligible and untouched.

## Correct behavior

- The run does not stop. `TASK-021` is recorded in the outcome note's **Blocked** section with
  classification `SPECIFICATION_INVALID` and what's actually contradictory — not silently dropped,
  not the whole run aborted over it.
- The agent does not pick an interpretation of the ambiguous requirement to make `TASK-021`'s tests
  pass and call it done. `NEEDS_REQUIREMENT_REVIEW` stays a human checkpoint even with no human
  watching this run in real time.
- `FIND READY TASKS` + `FILTER` re-run, and the loop proceeds to `TASK-022` (or whichever remaining
  task now scores highest) in the same run.
- The final outcome note shows `TASK-021` under Blocked and `TASK-022`/`TASK-023` under whatever
  their own outcomes were (Completed or Blocked) — a mixed-outcome run is the expected shape, not a
  failure of the skill.

## Walkthrough against current skill

The workflow's loop step is explicit: on `NEEDS_REQUIREMENT_REVIEW` (among the listed failure
routes) → "record to outcome note under Blocked, do not resolve it, continue the loop." Non-fatal
blocker handling repeats this and names the specific danger — "do not invent a resolution to keep
the run going" — directly addressing failure mode (b), not just (a). The loop's re-run of `FIND
READY TASKS + FILTER` after every completion (success or blocked) is what lets `TASK-022`/
`TASK-023` proceed without depending on `TASK-021`'s outcome.

**Gap check:** the workflow diagram uses `develop-next`'s failure-handling table by reference
rather than restating all nine classifications inline — confirmed this doesn't create a gap, since
`develop-next`'s own `Must not` list ("Produce its own final verification verdict") and its
existing failure-routing table already forces a classification decision before this skill's loop
ever sees the outcome; this skill only adds what happens *after* a classification is known.

## Verdict

**PASS.** No skill change needed beyond what's already written.
