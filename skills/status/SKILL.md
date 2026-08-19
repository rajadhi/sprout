---
name: status
description: Use when summarizing current project state — requirements, design, tasks, verification health, and the next recommended task, in a few lines
---

# status

## Overview

Concise project state, not a dump of every artifact. Should read like something a human can
scan in ten seconds.

**Announce at start:** "I'm using the status skill to summarize project state."

## Report shape

```
Requirements
<N> active, <N> unresolved

Design
<N> approved, <N> in review

Tasks
<N> total, <N> complete, <N> ready, <N> blocked, <N> verifying

Verification
<N>% first-pass, <N> escaped defects

Next:
TASK-XXX
Reason: <why this one, from the develop-next selection algorithm>
```

## Loop-health metrics

Compute from real data — `artifacts/verification-run.md` instances, `artifacts/approval.md`
instances, and task frontmatter — never estimate or round up from a small sample to sound more
mature than the data supports:

```
Loop health
<N>/<N> first-pass verification rate ( = runs with no prior FAIL run for the same task /
                                        total tasks with at least one run )
<N> retries (RETRY transitions across all runs)
<N> blocked, <N> retired
<N> human interventions (approval records — shape/design/ADR approvals, not every
                          implementation micromanagement)
<N> escaped defects (defects found after MERGED) vs. <N> caught pre-merge (e.g. a wrong
                      impact-analysis classification corrected before implementation started)
Median task size: <XS|S|M|L|XL> (over non-retired tasks)
Median verification run duration: <duration>, from recorded started_at/finished_at
                                   (note explicitly if these are approximate/unminstrumented)
```

**Be honest about sample size and precision.** With 1-2 real runs, "100% first-pass" is true but
not yet a meaningful trend — say so, don't present a tiny sample as if it were a stable rate.
Don't report a metric to more precision than the underlying data actually has (e.g. a "duration"
computed from hand-recorded timestamps is not the same as one measured by CI job timing).

## Must not

- Dump every artifact's full content
- Recommend a next task without applying the develop-next selection algorithm
- Report a metric derived from too small a sample as if it were a stable rate
- Round timestamps/durations to look more precisely measured than they are
