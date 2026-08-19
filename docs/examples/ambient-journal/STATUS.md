# Real `/sprout:status` output — Ambient Journal fixture

Not a hypothetical example report — every number below was pulled from the actual files in this
directory (`grep -H "^status:" *.md`, real dependency/size/risk fields).

> Updated after `docs/examples/ambient-journal/GRAPH-REQ-001.md` caught and corrected a real
> mistake: `TASK-009` was planned on an unchecked assumption and is now `RETIRED`, not `BLOCKED`.
> See that file's "What changed and why" for the full account.

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
0 complete
8 ready
0 blocked
1 retired (TASK-009 — its premise didn't hold, see GRAPH-REQ-001.md)
0 verifying

Verification
0 verification runs recorded against any Ambient Journal task yet
(tests/fixtures/toy-app has a real RUN-toy-001, modeled on TASK-003's AC-003-02, but it is a
separate proof fixture -- TASK-003.md's own verification_run field is still null, and this report
does not credit it as if TASK-003 were actually verified. First-pass % is not yet meaningful with
zero real runs against this task set.)

Next:
TASK-001
Reason: ties with TASK-002 on every scoring dimension (both S/R1, zero dependencies, both gate
the same 3 downstream tasks -- TASK-003, TASK-004, TASK-005 all depend on both). TASK-006 is
smaller (XS vs S) but blocks nothing downstream, so blocking_value/critical_path_weight outweigh
its size advantage per the selection algorithm (skills/develop-next/SKILL.md). TASK-001 wins the
tie against TASK-002 via the deterministic tie-break added during M3 pressure testing (lowest
task ID) -- not an arbitrary pick.
```

## How this was actually computed

```bash
grep -H "^status:" REQ-*.md DES-*.md TASK-*.md ADR-*.md
grep -E "^(status|size|risk|dependencies|implements|design|architecture):" TASK-*.md
```

Then applied `skills/develop-next/SKILL.md`'s selection algorithm by hand against the real
dependency graph above — the same reasoning `develop-next` would run, not a separate report
format.
