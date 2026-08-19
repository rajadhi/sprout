# Real loop-health metrics — Ambient Journal fixture

Computed from actual `APR-*.md`, `RUN-*.md`, and `TASK-*.md` files (commands below), per
`skills/status/SKILL.md`'s loop-health section. Sample size is tiny (2 real verification runs) —
presented honestly as such, not dressed up as a stable trend.

```
Loop health

Verification: 2/2 first-pass (100%)
  RUN-toy-001 (TASK-003 fixture) -- PASS, no prior FAIL recorded for that task
  RUN-toy-002 (TASK-006)         -- PASS, no prior FAIL recorded for that task
  Sample size is 2. This is a true ratio, not a meaningful trend yet -- both runs happen to be
  the only ones that exist. Do not extrapolate "100% first-pass" as a stable property of the
  framework from n=2.

Retries: 0 (no ENVIRONMENT_FAILURE -> RETRY transitions occurred)

Tasks: 0 blocked, 1 retired (TASK-009)

Human interventions: 4 (APR-00001 .. APR-00004 -- shape/design/ADR approvals, not
                        per-implementation-step micromanagement)

Defects: 0 escaped (none found after MERGED)
          1 caught pre-merge (TASK-009's false premise -- caught by re-running graph's impact
          analysis before any implementation was attempted, per GRAPH-REQ-001.md)

Median task size: S (over 8 non-retired tasks: XS x3, S x4, M x1 -- sorted median is S)

Median verification run duration: ~5 minutes, from RUN-toy-001/002's recorded started_at/
                                   finished_at. Caveat, stated explicitly: these timestamps were
                                   hand-recorded when each run's evidence file was written, not
                                   captured by any real clock instrumentation (no CI job timing,
                                   no wall-clock measurement around the actual test invocations).
                                   Treat as an approximate placeholder, not a measured duration --
                                   this is exactly the kind of over-precise-looking number
                                   skills/status/SKILL.md's "Must not" section warns against
                                   presenting as more precise than the underlying data supports.
```

## How this was actually computed

```bash
ls docs/examples/ambient-journal/APR-*.md | wc -l                     # 4
grep "^size:" docs/examples/ambient-journal/TASK-*.md                  # size distribution
grep "^status:" docs/examples/ambient-journal/TASK-*.md                # blocked/retired/merged
grep -E "^(started_at|finished_at|verdict):" tests/fixtures/toy-app/RUN-toy-00{1,2}.md
```

## Why this file exists

`docs/protocol.md` originally listed "loop-health observability/metrics" as v1 backlog — real
numbers require real runs to exist, and there were none yet at that point. Two now exist
(`RUN-toy-001`, `RUN-toy-002`), so this report is a real computation, not a hypothetical example
of what the report format would look like. The honest caveats above (tiny sample, unminstrumented
timestamps) are as much the point as the numbers — a metrics report that hides its own precision
limits would itself violate `docs/protocol.md` §1.7's evidence-over-assertion invariant.
