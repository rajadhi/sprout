---
name: develop-all-unattended
description: Use when the operator wants the whole READY backlog burned down unattended in one run, driven by Claude Code's /goal — runs develop-next repeatedly across every eligible task, never merges, never touches an R3/R4 task without approval, and leaves a note explaining what it did and how to redirect any decision through shape
---

# develop-all-unattended

## Overview

This is not a reimplementation of `develop-next` — it's `develop-next` run in a loop across the
whole `READY` backlog instead of once against a single task the operator picked. Every mechanic
(worktree, TDD, local verify, review, PR) is `develop-next`'s, reused verbatim. This skill adds
only: which tasks are eligible to run unattended, what happens when one of them hits a wall, and
what gets left behind when the run ends.

**Announce at start:** "I'm using the develop-all-unattended skill to work through the READY
backlog unattended."

**Intended invocation:** `/goal all eligible READY tasks reach PR_OPEN or are recorded blocked in
the run note, then stop` — Claude Code's `/goal` keeps the session working across turns and uses a
separate checker model to judge that condition, independent of this skill's own read of its
progress. This skill defines what "done" means for that checker; it doesn't implement `/goal`
itself.

## Workflow

```
LOAD PROJECT STATE
→ FIND READY TASKS
→ FILTER TO UNATTENDED-ELIGIBLE          (see below — a hard filter, not a scoring penalty)
→ LOOP, until no eligible task remains:
      → invoke develop-next's full workflow for one task (its own selection algorithm
        picks which one, same as a human-invoked run)
      → task reaches PR_OPEN               → record to outcome note under Completed
      → task hits NEEDS_REQUIREMENT_REVIEW, NEEDS_ARCHITECTURE_REVIEW, BLOCKED/HUMAN_REVIEW,
        or exhausts its bounded retries    → record to outcome note under Blocked, do not
                                              resolve it, continue the loop
      → re-run FIND READY TASKS + FILTER   (a finished PR can unblock a dependency; plan
                                              could add new READY tasks mid-run — never work
                                              off a stale snapshot from before the loop started)
→ WRITE OUTCOME NOTE
→ STOP                                    (this is /goal's completion condition)
```

**If `FIND READY TASKS` returns an empty set at any point** (including immediately, on the first
pass): this is not an error. Write the outcome note saying so and stop — do not treat "nothing to
do" as a failure requiring investigation.

## Filter to unattended-eligible

A hard filter, applied before the loop, and re-applied after every completed task:

- Exclude any `READY` task whose `risk` (`artifacts/task.md`) is `R3` or `R4` **unless** it already
  carries a non-null `approval_ref`. `project.yaml`'s `autonomy_policy` marks R3/R4 as
  `human_required`/`human_controlled` — this skill does not weaken that gate, it just refuses to
  attempt what it can't clear.
- Exclude anything `develop-next`'s own selection algorithm would already exclude on size grounds
  (`task_sizing_policy.autonomous_ceiling`, XL never eligible).

Excluded tasks go into the outcome note's **Excluded** section — never attempted, and never
silently reclassified (lowering a recorded risk or size to make a task eligible is exactly the kind
of thing this filter exists to prevent).

## Non-fatal blocker handling

A single blocked task is not a run failure. When a task's failure classification routes to
`NEEDS_REQUIREMENT_REVIEW`, `NEEDS_ARCHITECTURE_REVIEW`, or `BLOCKED/HUMAN_REVIEW` (per
`develop-next`'s failure-handling table), or its bounded `ENVIRONMENT_FAILURE` retries (cap 2) are
exhausted: record the task ID, the failure classification, and what's actually blocking it, then
move to the next eligible task. **Do not invent a resolution to keep the run going** — guessing at
a requirement clarification or an architecture call to unblock a task is exactly the failure mode
this skill exists to avoid; that's what makes it "on behalf of the operator" rather than "instead
of the operator."

## Outcome note

Written once, at the end of the run, to `artifacts/runs/<UTC-timestamp>-develop-all-unattended.md`
— plain markdown, not a governed artifact. It has no frontmatter schema, doesn't bump
`project.yaml`'s `schema_version`, and isn't parsed by `/sprout:graph`; it's a session report, not
an artifact-graph node.

Structure:

```markdown
# develop-all-unattended run — <UTC timestamp>

## Completed
- TASK-XXX — <PR link> — <one-line summary of the key implementation decision(s) made, pulled
  from the task's own Progress Log, never invented after the fact>

## Blocked
- TASK-XXX — <failure classification> — <what's blocking it, what would unblock it>

## Excluded
- TASK-XXX — <reason: R3/R4 without approval_ref | oversized>

## If you disagree with a decision above
Run `/sprout:shape` describing the concern and referencing the task ID above, rather than
hand-editing the PR directly — it comes back through the same review path as any other
requirement change.
```

If every task in the run ended up Blocked or Excluded (including the empty-backlog case), the note
still gets written — a run with nothing Completed is a real outcome, not a skipped step.

## Must not

- Attempt an R3/R4 task that lacks a valid `approval_ref`
- Merge any PR, or take any action past `PR_OPEN` — merge stays a human decision, same as every
  other Sprout flow
- Invent a resolution to a blocked task to avoid recording it as blocked
- Silently reclassify a task's recorded `risk` or `size` to make it eligible
- Skip the outcome note, even when every task failed or the backlog was empty
- Run tasks concurrently or across parallel worktrees — one task at a time, `develop-next`'s own
  selection order decides which, same as a human-driven run (`docs/protocol.md` §3 reserves
  concurrent multi-task execution for a future reconsideration, not this skill)
