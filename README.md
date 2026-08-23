# Sprout

Sprout is a Claude Code plugin that takes a rough idea and walks it through to shipped, working
code — write down what you want, get a requirement, a design if it needs one, a set of small
tasks, and then working, verified code — with a human approving the steps that actually matter.

## What Sprout is

- It keeps requirements, designs, and decisions as versioned files that don't get silently
  rewritten — change your mind later and it writes a new version, the old one stays in history
- It runs the actual coding loop (`/sprout:develop-next`): pick a task, build it, verify it, open
  a PR — using Claude Code's own skills and agents, plus Superpowers for the TDD/implementation
  work, not some separate agent runtime bolted on
- It won't call a task done just because an agent says it worked — it needs evidence first
- It mirrors its state into GitHub (issues, labels, branch protection), but GitHub isn't where the
  real state lives — Sprout's own files are

## What Sprout is not

- Not an app — it's the framework you install into one
- Not its own agent runtime, and not a graph database
- Not a router deciding which agent runs next (that's "graph engineering," in the 2026 sense of
  the term) — see [docs/protocol.md §3](docs/protocol.md) for why that's on purpose
- Not a fork of [Superpowers](https://github.com/obra/superpowers) — Sprout leans on it for
  TDD/implementation and stays responsible for the artifacts, evidence, and policy around it

## Install

Add Sprout as a Claude Code plugin to your project. Once installed, `/sprout:*` commands are
available.

**CLI, for local development:**

```
claude --plugin-dir /path/to/sprout
```

**CLI or Desktop app, for a persistent install:** this repo ships its own
`.claude-plugin/marketplace.json`, so it can be added as a single-plugin marketplace.

```
/plugin marketplace add /path/to/sprout
/plugin install sprout@sprout
```

In the Desktop app's Code tab, run those same two commands in the prompt box (they work there
too — no separate terminal needed), or use the **+** button → **Plugins** → **Add plugin** to
browse and install from your configured marketplaces once the marketplace above is added.

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

New ideas keep coming — run the loop again for each one; it never rewrites what's already been
accepted. Full walkthrough with expected output at each step:
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
/sprout:develop-all-unattended
                       run develop-next in a loop across the whole READY backlog (meant to be
                       driven by Claude Code's /goal) — never merges, never touches an R3/R4 task
                       without approval, leaves a run note plus a shape-based path to redirect
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
