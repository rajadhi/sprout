# Getting Started

## Install

Add Sprout as a plugin in your Claude Code project (marketplace or local path, per your usual
plugin installation flow). Once installed, `/sprout:*` commands are available.

## Bootstrap a project

```
/sprout:init
```

Detects whether your repo is new or already Sprout-initialized, asks only for genuinely unresolved
project context (name, purpose, platforms, stack, deployment environments, testing approach,
accessibility target, security/privacy constraints, autonomy policy, production approval policy —
unknowns are fine), and creates `.sprout/` plus the artifact directories. See
`skills/init/SKILL.md`.

## Add a thought

Drop raw, unstructured input anywhere Sprout can read it — `thoughts/2026-08-19-note.md`, a
meeting summary, a screenshot description. No format required; `shape` does the structuring.

## Shape it into a requirement

```
/sprout:shape
```

Reads your raw input, classifies it against existing requirements (new, clarification, bug,
contradiction, ...), generates a proposed requirement with acceptance criteria, runs it past the
`specification-critic` agent, and presents it for approval. You respond APPROVE / REJECT /
CLARIFY / EDIT. Approved requirements are immutable — a later change creates the next version, the
old one stays in history.

## Design it

```
/sprout:design
```

Only for requirements that need a UX/UI treatment. Self-critiques via `ux-critic` and
`accessibility-critic` before presenting an approval-ready candidate — you're not asked to review
every iteration, only the polished result.

## Plan tasks

```
/sprout:plan
```

Decomposes approved requirements/designs into small, independently verifiable, vertical-slice
tasks. Creates a GitHub issue automatically for every task that reaches `READY`.

## Develop

```
/sprout:develop-next
```

Picks the best ready task (not just the oldest), works it through an isolated branch, TDD,
implementation, and local verification using Superpowers for the mechanics, then hands off to a
PR.

## Verify

```
/sprout:verify
```

Runs the task's verification plan, captures evidence, and records an immutable verification run.
The `verifier` agent — not the implementer — decides whether the evidence actually proves the
acceptance criteria. Only a `PASS` verdict lets the task proceed toward merge.

## Check state

```
/sprout:status
```

Requirements, design, tasks, verification health, and the next recommended task — a few lines,
not a dump.

## Inspect relationships

```
/sprout:graph TASK-071
/sprout:graph REQ-024-v2
```

Upstream/downstream relationships for any node, including impact analysis when a requirement
changes — what's invalidated, needs review, or is unaffected downstream.

## The loop repeats

New thoughts arrive continuously — the cycle above (`shape → design → plan → develop-next →
verify`) runs again for each one, without ever rewriting prior accepted history. See
`docs/protocol.md` §9 for the full lifecycle and current milestone status.
