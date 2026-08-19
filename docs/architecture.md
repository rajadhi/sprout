# Sprout Architecture

How Sprout is built, not what it produces — see `docs/protocol.md` for the lifecycle and
artifact model. This document covers the plugin's own components and how they fit Claude Code's
native extension model.

---

## 1. Plugin

Sprout is a standard Claude Code plugin: `.claude-plugin/plugin.json` at the repo root, with
`skills/`, `agents/` at the plugin root alongside it — not nested inside `.claude-plugin/`. This
matters because Claude Code's plugin loader expects component directories at the plugin root.

Installed into a downstream project repo, Sprout's commands become namespaced: `/sprout:init`,
`/sprout:shape`, etc. — avoiding collision with other installed plugins' commands.

**Known constraint:** plugin-shipped agents don't support `hooks`, `mcpServers`, or
`permissionMode` fields. Consequence: general reusable behavior lives in plugin skills/agents; MCP
integrations and sensitive permissions are supplied by the *project* (via its own `.mcp.json` and
settings), not owned by the plugin. Sprout does not assume it can directly configure every
external tool a downstream project needs.

## 2. Skills

8 skills (`skills/*/SKILL.md`), each a single responsibility with a documented workflow, an
approval/critique gate where relevant, and explicit "must not" boundaries. See
`docs/protocol.md` §5 for the full command surface and what folded into what (`sync-github` into
`plan`, `diagnose` into `develop-next`, `impact` into `graph`).

Skills are process logic, not implementation code — they get pressure-tested the same way
application code gets unit-tested: adversarial scenarios where an inadequate skill would produce
the wrong behavior (invent a fact, silently resolve a contradiction, skip an approval gate).
`tests/scenarios/` holds these once M2 starts.

## 3. Agents

6 subagents (`agents/*.md`), each narrow and read-only, each running in **isolated context** —
this is deliberate, not incidental. A critic that saw another critic's output, or the
implementer's own summary of their work, would anchor on it and lose the independence that makes
a critique worth having. See `docs/protocol.md` §2 for why only `verifier` merges two of the
original brief's seven roles.

## 4. Artifact graph, not an execution graph

The artifact graph (`artifacts/*` frontmatter — `implements:`, `design:`, `supersedes:`, etc.) is
a **static data model** for provenance and impact analysis, parsed on demand by `/sprout:graph`.
It is not a runtime execution topology routing agent calls between nodes — that's 2026-sense
"graph engineering," and Sprout deliberately doesn't do it. The human invoking each command is the
router. See `docs/protocol.md` §3 for the full reasoning.

What Sprout *does* implement is loop engineering: `/sprout:develop-next` runs one task through a
self-driving cycle (`READY → ... → PR_OPEN`) with evidence-gated stop conditions, not manual
step-by-step prompting for each sub-action.

## 5. Hooks

Used sparingly, only for deterministic enforcement that doesn't need LLM judgment. One real hook
exists: `hooks/check-immutable-artifacts.py`, a `PreToolUse` hook on `Edit|Write` that enforces
§1.5's immutability invariant mechanically rather than relying on every skill to remember it.
Concretely:

- `APR-*.md` / `RUN-*.md` / `EVD-*.md` (approval, verification-run, evidence records) are denied
  any edit the moment they exist on disk — these have no legitimate post-creation edit, ever.
- `REQ-*.md` / `DES-*.md` / `ADR-*.md` / `DEC-*.md` whose on-disk `status:` is already
  `APPROVED`/`SUPERSEDED`/`VERIFIED`/`ACCEPTED` may only have `status`, `supersedes`,
  `superseded_by`, `approved_at`, or `approval_ref` change — a state-machine transition, not a
  rewrite. Any body edit, or an edit to any other frontmatter field, is denied with a message
  pointing at creating a new version file instead.
- Everything else (tasks, intents, not-yet-approved drafts) is unrestricted.

Verified against 6 real cases (`tests/hooks/test_check_immutable_artifacts.py`, run in CI as
`hook-tests`): 3 real denials (hard-immutable edit, body edit on a superseded requirement,
unallowed-field edit on an approved design) and 3 real allowances (status-field transition,
editing an unrestricted task, creating a brand-new versioned file) — not just written to look
correct, actually invoked as a subprocess against real fixture files with asserted exit codes.

This is a backstop, not a substitute for the main skill workflow — `shape`/`design` should never
attempt to edit an approved artifact in the first place. The hook exists for the case where they
(or a human, or a different agent) try to anyway.

## 6. MCP

Sprout bundles no MCP servers of its own. Downstream projects supply what they need (GitHub,
Supabase, browser, deployment, observability) and Sprout's skills detect and adapt to what's
available rather than requiring one vendor-specific integration in the framework core.

## 7. GitHub

A projection surface, not the source of truth — canonical state lives in `.sprout/` and the
artifact tree in the downstream repo. `plan` creates issues automatically when a task reaches
`READY`, applying this label set:

```
sprout:type:product   sprout:type:ux   sprout:type:engineering   sprout:type:architecture
sprout:state:ready   sprout:state:in-progress   sprout:state:verification
sprout:state:blocked   sprout:state:verified
sprout:risk:R0 .. sprout:risk:R4
sprout:size:XS   sprout:size:S   sprout:size:M   sprout:size:L   sprout:size:XL
```

### Label mechanics

Labels must exist before an issue can carry them — `gh issue create --label` fails silently-ish
(a clear error, but a real one) on a label that was never created. `init` (or `plan`'s first run
in a project) creates the full set idempotently via `gh label create --force`, which both creates
missing labels and is safe to re-run:

| Label | Color | Description |
|---|---|---|
| `sprout:type:product` | `#1D76DB` | Product-facing requirement |
| `sprout:type:ux` | `#8E44AD` | UX/design-facing requirement |
| `sprout:type:engineering` | `#5D6D7E` | Engineering-only, no product-facing change |
| `sprout:type:architecture` | `#154360` | Architecture/ADR-driven |
| `sprout:state:ready` | `#0E8A16` | Task ready for `develop-next` |
| `sprout:state:in-progress` | `#FBCA04` | Task claimed, being implemented |
| `sprout:state:verification` | `#D93F0B` | Task in verification |
| `sprout:state:blocked` | `#B60205` | Task blocked on a prerequisite |
| `sprout:state:verified` | `#0B6E4F` | Task verified, awaiting merge |
| `sprout:risk:R0` .. `sprout:risk:R4` | green → red gradient | Autonomy risk class, see `project.yaml` |
| `sprout:size:XS` .. `sprout:size:XL` | light → dark gray | Task size |

`plan` step 10, concretely:

```bash
gh issue create --title "$TASK_TITLE" \
  --body "Sprout task: $TASK_ID. Canonical artifact: artifacts/task.md (or the downstream
project's tasks/$TASK_ID.md). This issue is a projection — do not treat its text as the
source of truth; edit the task artifact and re-sync instead." \
  --label "sprout:type:$TYPE,sprout:state:ready,sprout:risk:$RISK,sprout:size:$SIZE"
```

Record the returned issue number on the task artifact's `github_issue:` field. On a later state
change (`READY` → `IN_PROGRESS` → ...), update labels via `gh issue edit --add-label
sprout:state:X --remove-label sprout:state:Y` — never close and recreate the issue, and never
push task-artifact content into the issue body as a rewrite (the issue body is set once at
creation; ongoing detail lives in the canonical artifact, the issue just links to it).

### Branch protection

Recommended/configured by Sprout but enforced entirely by GitHub's native controls — no skill may
override branch protection directly. This is the enforcement boundary: an unverified task cannot
merge through the normal GitHub path (M4 exit criterion). Minimum recommended ruleset via `gh api`
or the GitHub UI: required PR before merge, required status checks (the CI workflow's jobs),
required conversation resolution, no force-push, no branch deletion by non-admins. See
`.github/workflows/` for the checks branch protection should require.

## 8. CI/CD

GitHub Actions is the default substrate — no custom CI engine. Two distinct pipelines, don't
conflate them:

**Sprout's own repo** (`.github/workflows/ci.yml`) has no application code to lint/build/deploy —
it validates the plugin itself: `validate-structure` runs
`.github/scripts/validate_structure.py`, a small deterministic script (checks plugin manifest is
valid JSON, every skill/agent has required frontmatter — the kind of check §5 calls a hook
candidate, implemented here as a CI step since it needs to run on every push/PR, not just
locally); `toy-app-tests` runs the real unit tests in `tests/fixtures/toy-app`. Both required
status checks for branch protection.

**Downstream projects Sprout is installed into** get the fuller pipeline described in the
original design brief and still the right default to recommend: lint → typecheck → unit →
integration → build → security → deploy preview → runtime verification → evidence capture →
status check. Sprout doesn't generate this workflow file for a project automatically in v1 (that
would mean assuming a specific language/build toolchain, which §10 explicitly rules out) — `init`
documents the recommended shape, the project wires the actual commands for its own stack.

## 9. Computer-use

High-power tooling with a different trust boundary than sandboxed commands — treated accordingly.
Sprout never silently enables it, always declares when a verification scenario needs it, names
the specific application being controlled, captures evidence of the interaction, and provides a
clean stop path. Fallback for GUI functionality that APIs and dedicated tools can't adequately
verify — prefer precise browser/API tools where available. Backlog item, arrives after M4.
