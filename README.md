# Sprout

A Claude Code plugin: an AI-native engineering framework for moving from unstructured human intent
to verified, evidenced, merged change.

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

## Bootstrap

```
/sprout:init
```

See [docs/getting-started.md](docs/getting-started.md) for the full walkthrough.

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

- [docs/protocol.md](docs/protocol.md) — full v1 specification: invariants, artifact model,
  command surface, milestones
- [docs/architecture.md](docs/architecture.md) — how the plugin fits Claude Code's extension model
- [docs/getting-started.md](docs/getting-started.md) — command-by-command walkthrough

## Status

M1 (protocol + scaffolding) in progress. See [docs/protocol.md §9](docs/protocol.md) for the
milestone plan.

## License

MIT — see [LICENSE](LICENSE).
