# Real `/sprout:graph REQ-001-v2` output — Ambient Journal fixture

Every edge below was pulled from actual frontmatter fields (`grep`), not asserted. Traversal
matches `skills/graph/SKILL.md`'s described output shape: source intent, previous requirement
version, current design, architecture, tasks, tests, verification, released versions.

> **This is the corrected version of this report.** The first run of this query (when this
> requirement was first approved) asserted `DES-001` needed revision because it "referenced the
> dropped location signal." That claim was never actually checked against `DES-001-v1`'s real
> content — re-running this query properly (grepping the actual file instead of reasoning from
> the requirement diff alone) found zero mentions of location anywhere in `DES-001-v1.md`. See
> "What changed and why" below.

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
      requirements: [REQ-001, REQ-002, REQ-003]  <- covers this requirement. Written
      signal-agnostically (consent prompt/signal indicator described generically as "that
      signal" / "which signals," never enumerating photo/calendar/location as a fixed list) --
      it does not need a v2 for the signal-set reduction. Confirmed by `grep -c -i location
      DES-001-v1.md` = 0.

  architecture:
    ADR-001 (ACCEPTED)
      requirements_affected: [REQ-001]

  tasks (implements: [REQ-001]):
    TASK-004  READY     (empty state, AC-001-02)
    TASK-005  READY     (draft generation, AC-001-01/03, also implements ADR-001)
    TASK-006  READY     (enforce dropped signal, AC-001-04 -- exists specifically because of v2)
    TASK-009  RETIRED   (was: "remove location UI" -- moot, see below)

  tests / verification:
    none recorded yet -- every remaining task above has verification_run: null

  released versions:
    none -- nothing has merged yet for this requirement
```

## Impact analysis (the graph query that matters most here)

Given the change `REQ-001-v1 -> REQ-001-v2`, classify every downstream node:

```
DES-001-v1        UNAFFECTED       (signal-agnostic by design; grep-confirmed zero location
                                     references -- no revision needed)
TASK-004          LIKELY_UNAFFECTED  (empty state doesn't reference any specific signal)
TASK-005          NEEDS_REVIEW     (must not reference location in generation logic -- verify
                                     scope, since v1 planning assumed 3 signals, v2 has 2)
TASK-006          UNAFFECTED       (created for v2 specifically, already correct)
TASK-009          RETIRED          (its entire premise -- a location reference in DES-001 to
                                     remove -- doesn't exist; nothing to build)
ADR-001           LIKELY_UNAFFECTED  (trigger-reliability decision doesn't depend on which
                                     signals are in scope, only that generation happens)
```

Not blanket `INVALIDATED` across the board, per `skills/graph/SKILL.md`'s explicit rule against
that — each node gets real judgment based on what it actually depends on.

## What changed and why (correcting the first run of this query)

The original impact analysis, written when `REQ-001-v2` was approved (`APR-00003`'s notes),
classified `DES-001` as `NEEDS_REVIEW` based on reasoning from the requirement diff — "location
was dropped, so the design that mentions it must need updating" — without actually opening
`DES-001-v1.md` to check whether it mentioned location at all. It didn't. `TASK-009` was planned
on top of that unchecked assumption.

Running this query again, for real (`skills/graph/SKILL.md`'s own rule: *"grounded in the actual
current content of the downstream artifact, not an assumption about what it probably
contains"*, added specifically because of what this correction found), caught it.

**`REQ-001-v2.md` and `APR-00003.md` are not edited to fix this** — both are `APPROVED`-locked,
enforced for real by `hooks/check-immutable-artifacts.py` (confirmed: attempting to edit
`REQ-001-v2.md`'s body returns exit 2, "immutable once approved"). They stay exactly as they were
approved, including the imperfect analysis — that's correct: an approval record documents what
was believed *at approval time*, not a running best-guess that gets silently touched up later.
The correction lives here instead, in a freshly regenerated graph query, and in `TASK-009.md`'s
own retirement record. This is the immutability invariant actually constraining a real editorial
decision, not just a documented principle nobody tested against pressure.

`docs/protocol.md` §7 gained a 13th task state, `RETIRED`, specifically because there was
previously no correct state for "this task's premise turned out false" — `BLOCKED` implies it'll
become workable once its dependency resolves, which isn't true here; nothing about `TASK-009`
will ever become workable, because there's nothing left to build.

## How this was actually computed

```bash
grep -E "^(source_intent|supersedes|superseded_by|approval_ref):" REQ-001-v1.md REQ-001-v2.md
grep -c -i "location" DES-001-v1.md    # = 0, the actual correction
grep "requirements_affected" ADR-001.md
grep -l "implements: \[REQ-001\]" TASK-*.md
```
