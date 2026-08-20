# Scenario: agent's context is lost or compacted mid-task, then resumed

**Tests:** `skills/develop-next/SKILL.md` — `CHECK PROGRESS LOG` step, "Progress log and resuming".
**Failure mode being prevented:** a task is partway through `develop-next`'s workflow (worktree
created, RED test committed) when the driving agent's context is lost — compaction, session
restart, crash. A fresh invocation picks the task back up with no memory of what happened. An
inadequate `develop-next` either (a) ignores any record of prior progress and restarts from
scratch, silently redoing completed work (wasted effort, or worse, a second worktree/branch for
the same task), or (b) trusts a progress log's claims at face value without checking they still
hold, or (c) treats "we already logged past CHECK STALENESS" as a reason to skip re-checking it —
missing a supersession that happened in the gap between the crash and the resume.

## Input

`TASK-011` (persist draft locally before generation) has a `## Progress Log` recording:

```
- [2026-08-20T09:10] worktree created: branch task-011-local-persist
- [2026-08-20T09:22] baseline captured: 0 pre-existing failures
- [2026-08-20T09:41] RED committed: test_draft_persists_before_generation_call
```

The agent's session ended there (context compaction). A new `develop-next` invocation selects
`TASK-011` again — with none of the prior session's context, only the task file and repo state.
Two complications planted in this scenario: (1) the logged branch was rebased and force-pushed by
a human afterward, so the logged commit no longer exists on the branch — the log's claim is stale;
(2) `TASK-011`'s upstream requirement gained a new approved version after the RED commit was
logged.

## Correct behavior

- `CHECK PROGRESS LOG` finds the existing log and treats this as a resume, not a fresh start — it
  must not blindly recreate the worktree or re-write the already-logged RED test from nothing.
- Before continuing from the logged phase, it must verify the log's claim against reality: check
  the branch and the logged commit. Here that check fails (the commit is gone after the rebase) —
  this must be treated as `IMPLEMENTATION_ERROR` and routed to diagnose/retry, not silently
  papered over by re-deriving a new commit and pretending continuity, and not trusted as still
  green.
- Independent of the branch-state finding, `CHECK STALENESS` must still run — the log having
  already logged a phase past worktree creation is not a reason to skip it. Here it must catch the
  requirement's new approved version and halt before implementing further, per the existing
  staleness behavior.

## Walkthrough against skill before this change

Before the progress-log mechanism existed, `develop-next` had no way to represent "this task is
partway done" at all — `CHECK STALENESS` and worktree creation ran fresh every time regardless of
prior sessions, so mid-task context loss was invisible to the skill; a resumed run looked
identical to a fresh one and would recreate a second worktree/branch for the same task, with no
mechanism to notice or reconcile the abandoned first attempt.

**Gap found.** Fixed: added `CHECK PROGRESS LOG` as an explicit step right after task selection,
required re-verification of any logged claim against reality before trusting it (never blind
resume), and made `CHECK STALENESS` explicitly unconditional on resume — see "Progress log and
resuming" in `skills/develop-next/SKILL.md`.

## Verdict

**RED → GREEN.** See `skills/develop-next/SKILL.md` — `CHECK PROGRESS LOG` step and "Progress log
and resuming" section now define resume behavior, mandate re-verification over blind trust, and
keep `CHECK STALENESS` unconditional regardless of logged phase.
