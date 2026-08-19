# Real `/sprout:graph REQ-001-v2` output — Ambient Journal fixture

Every edge below was pulled from actual frontmatter fields (`grep`), not asserted. Traversal
matches `skills/graph/SKILL.md`'s described output shape: source intent, previous requirement
version, current design, architecture, tasks, tests, verification, released versions.

```
REQ-001-v2 (APPROVED)

  source_intent:
    INT-0001  (original raw input)
    INT-0002  (tester feedback that triggered this version)

  previous requirement version:
    REQ-001-v1 (SUPERSEDED)
      supersedes: null
      superseded_by: REQ-001-v2
      approval_ref: APR-00001

  this version:
    supersedes: REQ-001-v1
    superseded_by: null
    approval_ref: APR-00003

  current design:
    DES-001-v1 (APPROVED)
      requirements: [REQ-001, REQ-002, REQ-003]  <- covers this requirement, but stale: written
      before the v1->v2 supersession, still references the dropped location signal in its
      consent-prompt/signal-indicator sections. Impact analysis in APR-00003 classifies this as
      NEEDS_REVIEW, not INVALIDATED -- the flow structure holds, specific elements need updating.

  architecture:
    ADR-001 (ACCEPTED)
      requirements_affected: [REQ-001]

  tasks (implements: [REQ-001]):
    TASK-004  READY    (empty state, AC-001-02)
    TASK-005  READY    (draft generation, AC-001-01/03, also implements ADR-001)
    TASK-006  READY    (enforce dropped signal, AC-001-04 -- exists specifically because of v2)
    TASK-009  BLOCKED  (remove location UI, AC-001-04 -- blocked on DES-001-v2, see above)

  tests / verification:
    none recorded yet -- every task above has verification_run: null

  released versions:
    none -- nothing has merged yet for this requirement
```

## Impact analysis (the graph query that matters most here)

Given the change `REQ-001-v1 -> REQ-001-v2`, classify every downstream node:

```
DES-001-v1        NEEDS_REVIEW    (flow structure holds; location-specific elements stale)
TASK-004          LIKELY_UNAFFECTED  (empty state doesn't reference any specific signal)
TASK-005          NEEDS_REVIEW    (must not reference location in generation logic -- verify
                                    scope, since v1 planning assumed 3 signals, v2 has 2)
TASK-006          UNAFFECTED      (created for v2 specifically, already correct)
TASK-009          NEEDS_REVIEW    (exists specifically to resolve the DES-001 staleness)
ADR-001           LIKELY_UNAFFECTED  (trigger-reliability decision doesn't depend on which
                                    signals are in scope, only that generation happens)
```

Not blanket `INVALIDATED` across the board, per `skills/graph/SKILL.md`'s explicit rule against
that — each node gets real judgment based on what it actually depends on.

## How this was actually computed

```bash
grep -E "^(source_intent|supersedes|superseded_by|approval_ref):" REQ-001-v1.md REQ-001-v2.md
grep "^requirements:" DES-001-v1.md
grep "requirements_affected" ADR-001.md
grep -l "implements: \[REQ-001\]" TASK-*.md
```
