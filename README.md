# Sprout

A Claude Code plugin: an AI-native engineering framework that turns unstructured human intent into
verified, evidenced, merged change — raw thought in, shipped and proven code out, with a human
approving every consequential step along the way.

## What Sprout is

- A protocol for immutable, versioned requirements, designs, and decisions
- A small-task execution loop (`/sprout:develop-next`) built on Claude Code's native skills,
  agents, and Superpowers — not a new agent runtime
- An evidence-gated verification model: a task cannot reach `VERIFIED` because an agent believes
  it worked
- A GitHub projection: issues, labels, and branch protection reflect Sprout's canonical state,
  they don't replace it

## What Sprout is not

- Not an application — it's the engineering framework you install into one
- Not an alternative agent runtime or a graph database product
- Not an execution-topology router (2026-sense "graph engineering") — see
  [docs/protocol.md §3](docs/protocol.md) for why that's deliberate
- Not a fork of [Superpowers](https://github.com/obra/superpowers) — Sprout depends on it for
  TDD/implementation mechanics and stays responsible for immutable artifacts, evidence, and policy

## Install

Add Sprout as a Claude Code plugin to your project. Once installed, `/sprout:*` commands are
available.

## Quick start

```
/sprout:init
```

Bootstraps `.sprout/` and asks only for genuinely unresolved project context — unknowns are fine.
From there the loop runs on repeat, one command at a time, each gated by human approval where it
matters:

```
/sprout:shape          raw intent → approved, immutable requirement
/sprout:design         (if it needs a UX/UI treatment) → approved, immutable design
/sprout:plan           requirement/design → small vertical-slice tasks, GitHub issues auto-created
/sprout:develop-next   pick the best ready task, work it through TDD/implementation to a PR
/sprout:verify         run the task's verification plan, capture evidence, record a verdict
```

New raw thoughts arrive continuously — the loop above runs again for each one, without ever
rewriting prior accepted history. Full walkthrough with expected output at each step:
[docs/getting-started.md](docs/getting-started.md).

## Command reference

```
/sprout:init          bootstrap a project
/sprout:shape         raw intent → proposed, then approved, immutable requirement versions
/sprout:design        accepted requirement(s) → critiqued, approved, immutable design version
/sprout:plan          accepted requirements/designs → small vertical-slice tasks; auto-creates
                       GitHub issues for tasks that reach READY
/sprout:develop-next  select one ready task, execute it (worktree → TDD → implementation →
                       local verify → PR), including its own diagnose/retry failure path
/sprout:verify        run a task's verification plan, capture evidence, record a Verification Run
/sprout:graph         inspect artifact-graph relationships for a node; includes impact analysis
/sprout:status         concise project state + next recommended task, plus loop-health metrics
/sprout:migrate        move a project's artifacts to a new Sprout schema_version without silently
                       reinterpreting pre-migration versions
/sprout:release        VERIFIED/MERGED work → RELEASE_CANDIDATE → STAGING → PRODUCTION_APPROVAL
                       → RELEASED, enforcing project.yaml's production_approval_policy
/sprout:doctor         audit artifact-tree integrity: dangling references, stale versions,
                       orphaned approvals, schema drift
/sprout:metrics        deeper loop-health breakdown than status's snapshot — trends, breakdowns
                       by risk class/requirement
```

## Lifecycle

```
raw intent → shape → approve → immutable requirement
                                     ↓
                                  design → approve → immutable design
                                     ↓
                                   plan → small vertical-slice tasks → GitHub issues
                                     ↓
                             develop-next → TDD → implementation → PR
                                     ↓
                                  verify → evidence → verdict
                                     ↓
                          merge (through protected GitHub controls)
                                     ↓
                              repeat, without rewriting history
```

The central rule: **never advance engineering state because an agent believes it's correct —
advance it because the required evidence and policy conditions are satisfied.**

## Documentation

- [docs/getting-started.md](docs/getting-started.md) — command-by-command walkthrough
- [docs/protocol.md](docs/protocol.md) — full v1 specification: invariants, artifact model,
  command surface, milestones
- [docs/architecture.md](docs/architecture.md) — how the plugin fits Claude Code's extension model

## Status

v1 complete, backlog cleared — see [docs/protocol.md §9](docs/protocol.md) for milestone
definitions and `git log` for the full account. Genuinely remaining: `/sprout:migrate` and
`/sprout:release` are specified but unexercised (no schema change or release has happened yet to
run them against), and native iOS/macOS computer-use verification is proven possible but not yet
executed end-to-end.

## License

MIT — see [LICENSE](LICENSE).
