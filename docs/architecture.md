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

Used sparingly, only for deterministic enforcement that doesn't need LLM judgment: validating
required artifact structure, detecting accidental edits to immutable artifacts, checking required
metadata exists, detecting commits that bypass Sprout state. Not a substitute for the main skill
workflow, and not present at all in M1 — the first hook candidates arrive with M3/M4 once there's
real state to protect.

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

Branch protection (required PR, required CI, no force-push, conversation resolution) is
recommended/configured by Sprout but enforced entirely by GitHub's native controls — no skill may
override branch protection directly. This is the enforcement boundary: an unverified task cannot
merge through the normal GitHub path (M4 exit criterion).

## 8. CI/CD

GitHub Actions is the default substrate — no custom CI engine. A typical PR flow: lint → typecheck
→ unit → integration → build → security → deploy preview → runtime verification → evidence
capture → status check. Arrives with M4; not part of M1 scaffolding.

## 9. Computer-use

High-power tooling with a different trust boundary than sandboxed commands — treated accordingly.
Sprout never silently enables it, always declares when a verification scenario needs it, names
the specific application being controlled, captures evidence of the interaction, and provides a
clean stop path. Fallback for GUI functionality that APIs and dedicated tools can't adequately
verify — prefer precise browser/API tools where available. Backlog item, arrives after M4.
