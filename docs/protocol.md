# Sprout Protocol (v1, tightened)

Sprout is a Claude Code plugin: an AI-native engineering framework for moving from unstructured
human intent to verified, evidenced, merged change — without an alternative agent runtime, a
graph database, or a custom orchestration engine.

This document is the tightened v1 specification. It keeps every non-negotiable invariant from the
original design brief and cuts structural bloat (duplicate schema/template pairs, one-command-per-
noun sprawl, a formal verification-level taxonomy) that added file count without adding behavior.

---

## 1. Non-negotiable invariants (unchanged)

1. **Plugin, not runtime.** Skills, agents, hooks, MCP, Git, GitHub, GitHub Actions, Superpowers —
   nothing custom unless no native capability covers it.
2. **No graph database in v1.** The artifact graph is typed metadata in versioned repo artifacts —
   a data model, not an execution engine. See §3 for why it stays that way.
3. **GitHub is a projection, not the source of truth.** Canonical state lives in `.sprout/` and the
   artifact tree.
4. **Accepted artifacts are immutable.** Changes create new versions or new entities; never
   overwrite in place.
5. **Small changes are a first-class invariant.** A task with multiple unrelated outcomes must be
   decomposed before implementation.
6. **Evidence is mandatory.** A task cannot reach `VERIFIED` because an agent says it worked.
7. **Human approval is policy-driven**, not default-on for every action.
8. **Product correctness ≠ implementation correctness.** Passing tests don't prove the right
   product behavior.
9. **The framework is testable.** Skills are process logic and get pressure-tested like any other
   software, RED → GREEN → REFACTOR against agent *behavior*, not code.

The central rule (keep this posted everywhere):

> Never advance engineering state because an agent believes it's correct. Advance it because the
> required evidence and policy conditions for that transition are satisfied.

```
Requirement → Acceptance Criteria → Implementation → Verification Run → Evidence → Verdict → State transition
```

---

## 2. What changed from the original brief, and why

| Area | Original | Tightened | Why safe |
|---|---|---|---|
| Commands | 11 | 8 | `sync-github` folds into `plan` (issue created automatically when a task hits `READY`); `diagnose` folds into `develop-next`'s failure path (it was never a thing a human invokes directly); `impact` folds into `graph` (impact analysis is a graph query + classification, not a separate capability). `design` stays separate — different critics, different approval gate, genuinely distinct phase. |
| Agents | 7 | 6 | Only `verification-agent` + `evidence-reviewer` merge, into `verifier` — both are post-implementation, same trust tier, non-adversarial to each other, and one directly consumes the other's output. Every agent whose value depends on **isolated, independent judgment** (`specification-critic`, `ux-critic`, `accessibility-critic`, `architecture-reviewer`, `implementation-reviewer`) stays separate — collapsing those into one parametrized agent would contaminate each pass with the last and defeat the point of having a critic at all. |
| Schemas + templates | 11 + 11 files | 9 template files | A template *is* a schema with placeholders filled in (YAML frontmatter + body). No project has ever needed the abstract schema separately from the concrete template — merge them. `acceptance-criterion` drops from a standalone artifact type to an inline list field on `requirement`/`task` (still individually addressable by ID, just not a separate file). |
| Policies | 6 separate YAML files | fields inside `project.yaml` | Task-sizing, autonomy, verification, evidence, and merge policy are config values. They become standalone files only once a real project needs to override one independently — YAGNI until then. |
| Verification levels | 10-level numbered taxonomy | a `checks:` list on the task's verification plan | The numbered levels (lint, unit, integration, contract, build, deploy, runtime, computer-use, visual, review) still exist as *possible check types* — they just don't need ceremony as a taxonomy. The task's verification plan already has to enumerate which checks apply; a flat list does that with less indirection. A `security` check type was added to the list during M3 dogfooding — the original brief's evidence types include `SECURITY_RESULT` but no verification level ever named a `security` check, an inconsistency inherited from the original 10-level taxonomy and only caught by actually writing a task that needed one. |
| Requirement state machine | 10 states | 6 states | `NEEDS_INPUT` becomes a status flag inside `SHAPING`, not a separate state. `ACTIVE` / `IMPLEMENTED` / `VERIFIED` move to the **task** state machine, where they belong — a requirement itself isn't implemented or verified, its tasks are. |
| Task/implementation state machine | 12 states + failure paths | unchanged | This is the real control loop. Nothing here is decorative — every state is a distinct, evidence-relevant checkpoint. Trimming it would cut the invariant, not the bloat. |
| Directory structure | 8 top-level dirs | 5 top-level dirs | `schemas/`, `templates/`, `policies/` → `artifacts/` (merged templates with embedded schema + default policy values). `references/` folds into `docs/`. |
| Phases | 14 phases | 4 milestones | Each original phase was a real checkpoint but too granular to plan against. Grouped into 4 milestones, each independently dogfoodable and each ending with a concrete exit criterion, matching the brief's own instruction (§79) not to build the whole framework in one pass. |
| Execution model | implied "graph engineering" as a named methodology principle | dropped; loop engineering only | See §3 — the original brief's Ambient Journal fixture listed `graph_engineering` as a methodology alongside `loop_engineering`. Cut. |

Untouched because they were already tight and correct: the artifact graph (typed nodes/edges as
plain metadata, described in §7), the non-goals list (§10), Superpowers integration mapping,
computer-use policy, evidence privacy/redaction rules, branch protection recommendations.

---

## 3. Loop engineering, not graph engineering

As of August 2026, "loop engineering" and "graph engineering" are distinct, current terms in
agentic system design — worth being precise about which one Sprout actually is, since the
original brief used both loosely.

**Loop engineering** (coined June 2026): designing agent loops that run themselves — an agent
reasons, acts, observes, and iterates toward a goal until a stop condition is met, replacing
manual step-by-step prompting. This is exactly what `/sprout:develop-next` does: one task travels
`READY → CLAIMED → IMPLEMENTING → LOCAL_VERIFICATION → PR_OPEN → ...` as a single self-driving
cycle, stopping only when evidence says so. **Sprout is loop-engineered.** This is real and load-
bearing — keep it.

**Graph engineering** (emerged mid-to-late 2026, framed as the layer beyond loop engineering):
treating agent workflow as an explicit *execution* topology — nodes are agents/tools, edges are
runtime control-flow/routing decisions between them, with typed handoff contracts and a
deterministic policy router deciding what runs next. This solves problems that arise when
multiple agents/tools coordinate concurrently and routing itself gets complex.

**Sprout deliberately does not do this, and shouldn't.** Its flow is a human invoking one command
at a time against one task — the human *is* the router, on purpose (§1.7/§1.8: humans gate
consequential transitions; agents don't self-route past them). Adding a deterministic routing
hook that auto-advances the task state machine would be solving a coordination problem Sprout
doesn't have, at the cost of quietly weakening the human-approval-gate invariant. If Sprout later
needs unattended, concurrent, multi-task execution, this is worth revisiting — not before.

What Sprout *does* have, and keeps, is the **artifact graph**: a static data model (typed
nodes/edges as versioned file metadata: requirement↔design↔task↔evidence) used for provenance
and impact analysis, queried by `/sprout:graph`. This is not graph engineering in the 2026 sense —
it's closer to a lightweight knowledge graph. Calling it that from here on avoids the confusion.

---

## 4. Terminology (mostly unchanged)

Intent, Requirement, Design, Decision, Task, Acceptance Criterion, Verification, Evidence,
Verification Run, Approval, Loop — definitions as in the original brief, §2. Not repeated here to
avoid drift between two copies; this file is the only copy.

**Artifact Graph** (renamed from "Graph"): the typed network of relationships between the above
entities, represented as metadata in versioned files — a data model for provenance and impact
analysis, not an execution topology. See §3.

---

## 5. Command surface (12)

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
                       (what's affected by a change to this node, classified INVALIDATED /
                       NEEDS_REVIEW / LIKELY_UNAFFECTED / UNAFFECTED)
/sprout:status         concise project state + next recommended task, including loop-health
                       metrics computed from real verification runs (see §5.1)
/sprout:migrate        move a project's artifacts to a new Sprout schema_version, preserving
                       pre-migration versions rather than reinterpreting them silently
/sprout:release        VERIFIED/MERGED work → RELEASE_CANDIDATE → STAGING → PRODUCTION_APPROVAL
                       → RELEASED, enforcing project.yaml's production_approval_policy
/sprout:doctor         audit artifact-tree integrity: dangling references, stale version
                       references, orphaned approvals, schema drift, out-of-band immutable edits
/sprout:metrics        deeper loop-health breakdown than status's snapshot — trends, breakdowns
                       by risk class/requirement, once enough verification-run history exists
```

The original v1 target was 8; `migrate`/`release`/`doctor`/`metrics` were originally scoped as
backlog and built once real verification-run history existed to make them meaningful rather than
speculative (see §9's milestone history for when each landed).

---

## 6. Agents (v1: 6)

```
specification-critic     — ambiguity, contradictions, invented assumptions in shaped requirements
ux-critic                 — usability of a design candidate
accessibility-critic      — accessibility of a design candidate
architecture-reviewer     — challenges consequential technical decisions / ADRs
implementation-reviewer   — reviews implementation against task + requirement (author ≠ reviewer)
verifier                  — executes verification scenarios AND judges whether evidence proves
                             the acceptance criteria (merged verification-agent + evidence-reviewer)
```

Each stays narrow. No agent owns more than one lens. `verifier` is the only merge, and only
because both halves are same-tier, sequential, and not adversarial to each other — see the table
in §2 for why the rest don't merge.

---

## 7. Artifact model (v1: 9 templates, schema embedded as frontmatter)

```
artifacts/
├── project.yaml         project profile + embedded policy (autonomy, task-sizing, verification,
│                        evidence, merge) with sane shipped defaults
├── intent.md            append-only raw input
├── requirement.md        problem/outcome/scope/non-goals/acceptance criteria (inline)/...
├── design.md             user flow/states/accessibility/... tied to requirement(s)
├── decision.md           ADR: problem/options/decision/rationale/consequences
├── task.md               purpose/requirement/design/ADR refs/acceptance criteria/verification plan
├── verification-run.md   run ID/commit/checks/evidence refs/verdict
├── evidence.md            manifest format: type/run/task/commit/env/timestamp/content/redaction
└── approval.md            immutable: artifact/actor/decision/timestamp/notes
```

The artifact graph (§4) lives as metadata fields inside these files (e.g. a task's `implements:`,
`design:`, `verification:` list). `/sprout:graph` parses the tree; no separate index or database
required for v1.

State machines (both unchanged in substance from the original brief):

**Requirement** (6 states): `PROPOSED → SHAPING → READY_FOR_REVIEW → APPROVED →
SUPERSEDED | RETIRED`. `NEEDS_INPUT` is a sub-status of `SHAPING`, not a distinct state.

**Task/Implementation** (12 states, unchanged) — this is Sprout's loop, per §3: `READY → CLAIMED
→ IMPLEMENTING → LOCAL_VERIFICATION → PR_OPEN → CI_VERIFICATION → RUNTIME_VERIFICATION →
EVIDENCE_CAPTURE → INDEPENDENT_REVIEW → VERIFIED → MERGED → RELEASED`, with failure paths
`VERIFICATION_FAILED → DIAGNOSING → IMPLEMENTING`, `SPECIFICATION_INVALID →
NEEDS_REQUIREMENT_REVIEW`, `ARCHITECTURE_INVALID → NEEDS_ARCHITECTURE_REVIEW`,
`SECURITY_FAILURE → BLOCKED/HUMAN_REVIEW`, `ENVIRONMENT_FAILURE → RETRY` (bounded — cap
2 attempts, never blind-loop; see `skills/develop-next/SKILL.md`).

**`RETIRED`** — a 13th state, added after dogfooding surfaced a real gap the original 12 never
covered: what happens to a planned task that turns out to be unnecessary, not because it failed
but because upstream reality changed underneath it? From any pre-`VERIFIED` state, a task moves to
`RETIRED` when `/sprout:graph`'s impact analysis (§7) determines its planned work no longer
applies — re-reading the actual upstream artifact (not just trusting an earlier assumption about
it) shows there's nothing left to build. `RETIRED` is terminal, same as `RELEASED`. The task
artifact stays — deleting it would erase the record of why it was planned and why it turned out
unnecessary, which is exactly the kind of history §1.5 says not to lose.

---

## 8. Repository structure (v1)

```
sprout/
├── .claude-plugin/
│   └── plugin.json
├── skills/
│   ├── init/SKILL.md
│   ├── shape/SKILL.md
│   ├── design/SKILL.md
│   ├── plan/SKILL.md
│   ├── develop-next/SKILL.md
│   ├── verify/SKILL.md
│   ├── graph/SKILL.md
│   ├── status/SKILL.md
│   ├── migrate/SKILL.md
│   ├── release/SKILL.md
│   ├── doctor/SKILL.md
│   └── metrics/SKILL.md
├── agents/
│   ├── specification-critic.md
│   ├── ux-critic.md
│   ├── accessibility-critic.md
│   ├── architecture-reviewer.md
│   ├── implementation-reviewer.md
│   └── verifier.md
├── artifacts/            (templates with embedded schema; see §7)
├── hooks/
│   ├── hooks.json
│   └── check-immutable-artifacts.py   (see docs/architecture.md §5)
├── docs/
│   ├── protocol.md        (this file)
│   ├── architecture.md
│   ├── getting-started.md
│   └── examples/
├── tests/
│   ├── scenarios/
│   ├── fixtures/
│   └── hooks/
├── .github/
│   ├── workflows/
│   └── scripts/
├── README.md
├── CLAUDE.md
└── LICENSE
```

Downstream project bootstrap (`.sprout/` inside a consuming repo) is unchanged from the original
brief §5 — `project.yaml`, `approvals/`, `state/`, `graph/`, `runs/`.

---

## 9. Milestones (v1: 4, replacing the original 14 phases)

**M1 — Protocol + scaffolding.** Plugin manifest, repo structure, artifact templates, state
machine docs (this file + architecture.md), default policy values. No orchestration logic.
*Exit:* a human can read the repo and understand the complete lifecycle.

**M2 — Shape + design loop.** Immutable requirement and design versioning; `specification-critic`,
`ux-critic`, `accessibility-critic`; approval records as artifact-graph edges, not status text.
*Exit:* messy raw input becomes an approved, immutable requirement + design version; changing it
produces a new version without touching history.

**M3 — Plan → develop-next → verify, integrated with Superpowers.** Vertical-slice task
decomposition; one task travels ready → isolated branch → TDD → implementation → independent
review → PR → evidence → recorded Verification Run.
*Exit:* a task cannot reach `VERIFIED` without a valid evidence bundle.

**M4 — GitHub projection + merge policy.** Issue creation on `READY`, label sync, branch
protection configuration, merge policy enforcement via GitHub's native controls (Sprout never
overrides branch protection directly).
*Exit:* an unverified task cannot merge through the normal GitHub path.

Backlog after M4, not blocking v1 completeness: computer-use verification, self-dogfooding as an
ongoing practice rather than a phase. `/sprout:migrate`, `/sprout:release`, `/sprout:doctor`, and
`/sprout:metrics` were originally scoped here too; all four are now built (§5) — `doctor` has a
real dogfooded run (`docs/examples/ambient-journal/DOCTOR.md`), `migrate`/`release` are specified
but not yet exercised (no schema change or release has happened yet to run them against for
real), `metrics` extends `status`'s loop-health section once there's more run history than the
current 2 real verification runs support. Loop-health observability itself moved out of backlog
once real verification runs existed to compute it from — see `skills/status/SKILL.md`'s
loop-health section and `docs/examples/ambient-journal/METRICS.md`.

---

## 10. Non-goals (unchanged from original brief §74, plus one addition)

No custom LLM router, agent runtime, graph database, Git hosting, CI system, deployment platform,
design editor, project-management UI, or vector database. No web dashboard unless a concrete
requirement emerges. No mandatory Supabase/Vercel/React/Swift. Sprout is the engineering
framework, not the product stack.

**No execution-graph router.** Per §3, Sprout does not adopt 2026-style graph engineering
(runtime routing between agent/tool nodes via typed handoff contracts). The human invoking each
command is the router. Revisit only if Sprout needs unattended, concurrent, multi-task execution.
