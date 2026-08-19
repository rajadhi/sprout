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

**v1 complete, then pushed past v1 into every remaining backlog item.** 12 skills, 6 agents, 9
artifact templates, 20 pressure scenarios, 1 real enforcement hook, 4 required CI checks, 19
GitHub labels, 14 merged PRs — every one gated by real CI on a real branch-protected repo, not a
description of what would happen.

- **M1–M4 (protocol, shape/design, plan/develop-next/verify, GitHub projection) — done.** See
  git history for the full account; the short version: every milestone shipped with pressure
  scenarios where applicable and a real dogfooded proof, not just prose. Real gaps found and
  fixed at every stage, including a genuine spec inconsistency (`checks:` never had a `security`
  type) and a real mistake in the framework's own reasoning (`TASK-009` retired after re-running
  `graph`'s impact analysis found its premise was false — see
  [GRAPH-REQ-001.md](docs/examples/ambient-journal/GRAPH-REQ-001.md)).
- **Immutability hook — real, not decorative.** `hooks/check-immutable-artifacts.py` genuinely
  blocks editing approved requirements/designs/decisions and any approval/verification/evidence
  record — confirmed by trying, including during the `TASK-009` correction, which had to route
  around it rather than through it.
- **Real GitHub enforcement.** Branch protection requires 4 CI checks (`validate-structure`,
  `toy-app-tests`, `hook-tests`, `risk-approval-check`) before merge — the last one closes a real
  gap: R3/R4 "human approval required" now has GitHub-enforced teeth
  (`.github/scripts/check_risk_approval.py`), not just trust. All 19 `sprout:*` labels exist for
  real on this repo.
- **Real Superpowers-integrated execution.** `TASK-006` traveled `READY → VERIFIED → MERGED` for
  real: a real `git worktree`, a dispatched subagent doing real TDD (honestly reporting when its
  first test scenario didn't actually produce RED and adding a real adversarial one instead), an
  independent verifier re-running the suite rather than trusting the report, a real merged PR.
- **Backlog cleared.** `/sprout:migrate`, `/sprout:release`, `/sprout:doctor`, `/sprout:metrics`
  all built (`doctor` dogfooded for real —
  [DOCTOR.md](docs/examples/ambient-journal/DOCTOR.md)). Loop-health metrics computed from real
  verification runs, honestly caveated for sample size and timestamp precision
  ([METRICS.md](docs/examples/ambient-journal/METRICS.md)). Computer-use/runtime verification's
  mechanism proven for real via a browser tool
  ([tests/fixtures/toy-ui](tests/fixtures/toy-ui)) — explicitly not overclaimed as native
  iOS/macOS verification, which Ambient Journal's actual UI tasks would need.

See [docs/protocol.md §9](docs/protocol.md) for the milestone definitions. Genuinely remaining:
`/sprout:migrate`/`/sprout:release` are specified but unexercised (no schema change or release
has happened yet to run them against), and native iOS/macOS computer-use verification is proven
possible but not yet executed end-to-end.

## License

MIT — see [LICENSE](LICENSE).
