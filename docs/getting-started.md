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

## Run it unattended with `/goal`

Claude Code's `/goal` command (see `docs/protocol.md` §3.1) sets a completion condition and keeps
Claude working turn after turn without you re-prompting, until a lightweight evaluator model
confirms the condition holds. It's a session-level continuation primitive, not a Sprout feature —
you invoke it directly, pointing it at a Sprout skill and a Sprout state as the condition.

**A single task through to a PR:**

```
/goal run /sprout:develop-next on TASK-042 until it reaches PR_OPEN with a PASS verdict
recorded in its verification-run, or it moves to a blocked/needs-review state -- stop after
25 turns
```

**Draining the whole ready queue:**

```
/goal work through every READY task with /sprout:develop-next, one at a time, until the READY
queue is empty or a task needs human review -- stop after 60 turns
```

**Turning a backlog of raw thoughts into requirements:**

```
/goal run /sprout:shape on every file under thoughts/ until each one either reaches
READY_FOR_REVIEW as a requirement or is explicitly recorded as an open question needing human
input -- never invent an acceptance criterion just to force resolution -- stop after 15 turns
```

Same pattern works non-interactively for scheduled/CI use: `claude -p "/goal ..."` runs the loop
to completion in one invocation (add `--output-format stream-json --verbose` to see progress
rather than waiting silently for the run to end).

**The evaluator checks the transcript, not your evidence.** `/goal`'s completion check is a small
model reading what Claude has said so far — it can't independently run tests or read files. Write
every condition against Sprout's own recorded state (a task's verification-run verdict, a
requirement's status field), never against Claude's own claim of being done. The actual proof
standard doesn't change: a task still needs a real `PASS` from the `verifier` agent, a requirement
still needs `specification-critic` to have run. `/goal` only removes the need to re-prompt between
turns — it isn't a second, weaker verification path alongside Sprout's evidence-gated one.
