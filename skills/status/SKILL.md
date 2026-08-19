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

Once loop-health metrics exist (backlog, not v1 — see `docs/protocol.md` §9), extend with:
first-pass verification rate, average retries, blocked tasks, human intervention count, escaped
defect rate, median task size, median cycle time.

## Must not

- Dump every artifact's full content
- Recommend a next task without applying the develop-next selection algorithm
