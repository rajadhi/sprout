# Real `/sprout:status` output — Ambient Journal fixture

Not a hypothetical example report — every number below was pulled from the actual files in this
directory (`grep -H "^status:" *.md`, real dependency/size/risk fields).

> Updated twice since the first run: (1) `GRAPH-REQ-001.md` caught and corrected a real mistake —
> `TASK-009` was planned on an unchecked assumption and is now `RETIRED`, not `BLOCKED`; (2)
> `TASK-006` has actually been implemented, verified, and merged for real — the first Ambient
> Journal task with a genuine `MERGED` status, not just a plan.

```
Requirements
3 active (REQ-001-v2, REQ-002-v1, REQ-003-v1)
0 unresolved
(REQ-001-v1 is SUPERSEDED, not counted as active — it's history, not open work)

Design
1 approved (DES-001-v1)
0 in review
(DES-001 is current, not stale -- an earlier version of this report incorrectly said otherwise;
see GRAPH-REQ-001.md for the correction and why it couldn't just be silently fixed in place)

Tasks
9 total
1 merged (TASK-006 -- real git worktree, real subagent TDD, real independent verification,
real merged PR: github.com/rajadhi/sprout/pull/6)
7 ready
0 blocked
1 retired (TASK-009 — its premise didn't hold, see GRAPH-REQ-001.md)
0 verifying

Verification
1 real verification run against an Ambient Journal task: RUN-toy-002 (TASK-006), PASS.
RUN-toy-001 (modeled on TASK-003's AC-003-02) remains a separate proof fixture, not credited to
TASK-003 itself -- that task's verification_run field is still null.
First-pass rate: 1/1 (100%) on the one real run so far -- not yet a meaningful sample size.

Next:
TASK-001
Reason: ties with TASK-002 on every scoring dimension (both S/R1, zero dependencies, both gate
the same 3 downstream tasks -- TASK-003, TASK-004, TASK-005 all depend on both). TASK-001 wins
the tie against TASK-002 via the deterministic tie-break added during M3 pressure testing
(lowest task ID) -- not an arbitrary pick. (TASK-006, which previously factored into this
comparison, is now MERGED and out of the ready pool.)
```

## How this was actually computed

```bash
grep -H "^status:" REQ-*.md DES-*.md TASK-*.md ADR-*.md
grep -E "^(status|size|risk|dependencies|implements|design|architecture):" TASK-*.md
```

Then applied `skills/develop-next/SKILL.md`'s selection algorithm by hand against the real
dependency graph above — the same reasoning `develop-next` would run, not a separate report
format.
