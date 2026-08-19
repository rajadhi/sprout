---
name: metrics
description: Use when a deeper loop-health breakdown is needed than status's current-snapshot section — trends over time, breakdowns by risk class or requirement, not a dashboard product
---

# metrics

## Overview

`/sprout:status`'s loop-health section is a current snapshot (see `skills/status/SKILL.md`).
`metrics` is the deeper cut once there's enough history to make trends meaningful: first-pass
rate over time (not just the current ratio), cycle time distribution, retry rate by risk class,
which requirement generated the most rework. Still a generated report — `docs/protocol.md` §10
rules out a custom dashboard/UI; this produces markdown/text, not a product.

**Announce at start:** "I'm using the metrics skill to produce a loop-health breakdown."

## Report shape

```
Trend (last N verification runs, or all if fewer than N exist)
First-pass rate: <trend, e.g. "60% -> 75% -> 100% over last 3 windows">
Retry rate by risk class: R0 <N>%, R1 <N>%, R2 <N>%, R3 <N>%, R4 <N>%

Cycle time
Median: <duration>
By task size: XS <duration>, S <duration>, M <duration>, L <duration>, XL <duration>

Rework
Requirement(s) with the most superseded versions: <REQ-XXX> (<N> versions)
Task(s) retired after being planned: <TASK-XXX> (<reason category>)

Sample size note: <N> total verification runs this report is based on.
```

## Honesty rules (same discipline as status's loop-health section)

- State the sample size prominently. A "trend" computed from 2-3 runs is not a trend — say that
  plainly rather than drawing a line through two points.
- Don't compute a rate/percentage from a denominator of zero or near-zero without flagging it.
- Don't report cycle-time precision the underlying timestamps don't actually have (hand-recorded
  vs. instrumented — see `docs/examples/ambient-journal/METRICS.md` for what that caveat looks
  like in practice).

## Must not

- Present a small sample as a stable trend
- Build or imply a dashboard/UI — this is a text report
- Compute a breakdown dimension (e.g. "by requirement") that has too few data points per bucket
  to mean anything, without saying so
