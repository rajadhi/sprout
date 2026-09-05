# Working in this repository

This is the Sprout plugin's own repository, not a project that uses Sprout. The rules below
govern changes to Sprout itself. See `docs/protocol.md` for the full specification these rules
enforce.

## Framework governance

Sprout changes are stricter than the application changes Sprout helps other projects make:

- **Skill change** → needs a pressure scenario in `tests/scenarios/` demonstrating the skill
  resists the failure it's meant to prevent (invented facts, silently resolved contradictions,
  skipped approval gates), not just a description of intended behavior.
- **Schema change** (artifact frontmatter shape) → bump `schema_version` in `artifacts/project.yaml`
  and don't silently reinterpret artifacts written under the old schema.
- **Policy change** (autonomy, task-sizing, verification, evidence, merge — the fields in
  `artifacts/project.yaml`) → needs explicit rationale in the commit message, not a silent edit.
- **Verification change** → regression-check against existing scenarios before merging.
- **Significant plugin change** (`skills/`, `agents/`, `hooks/`, `.github/scripts/`,
  `.github/workflows/`, `artifacts/`, `CODEOWNERS`) → bump `.claude-plugin/plugin.json`'s
  `version`. Default to a patch bump; bump minor or major only when explicitly asked to. This
  isn't optional convention — a real user hit the actual failure mode twice (shipped content
  with no version bump means Claude Code's plugin manager sees "already installed, nothing
  changed" and never refreshes an existing install, even after an explicit marketplace/plugin
  update and a forced reload) before `.github/scripts/check_plugin_version_bump.py` made it a
  required CI check instead of a thing to remember.

Never let Sprout silently weaken its own verification rules.

## Non-negotiables (see docs/protocol.md §1)

- Prefer native Claude Code capabilities → Skill → Agent → Markdown → YAML/JSON → GitHub native →
  GitHub Actions → MCP → existing CLI → tiny deterministic helper → custom executable code, in
  that order. Don't reach for custom code when a markdown skill or a YAML template does the job.
- No graph database. No custom agent runtime. No execution-topology router — the artifact graph
  is a data model, not a routing engine (docs/protocol.md §3).
- Small changes. A commit that bundles unrelated concerns should be split, even inside this repo.
- Don't invent product/framework decisions to fill gaps — flag unknowns instead of guessing, same
  discipline Sprout asks of `shape` and `init`.

## Commit discipline

Commit in the same small, logically-scoped chunks Sprout's own `plan` skill would produce for a
downstream project — one artifact type or one skill/agent group per commit, not one giant commit
per milestone. This repo dogfoods its own small-change invariant.

## Current milestone

v1 complete, backlog cleared — M1 through M4 plus all originally-backlog items done (see
`README.md` Status). Genuinely remaining: `/sprout:migrate`/`/sprout:release` are specified but
unexercised (nothing to run them against yet), native iOS/macOS computer-use verification is
proven possible but not executed end-to-end. Treat any future work with the same proof standard
established throughout: pressure scenarios plus something real, not descriptions of intended
behavior — and when a "real" proof surfaces a mistake in earlier work (see `TASK-009`'s
retirement), correct it through a new artifact, not a rewrite of history.

## Branch protection is live

`main` on github.com/rajadhi/sprout has real branch protection (required PR, required CI status
checks, no force-push — see `docs/examples/github-dogfood.md`). Direct pushes from the repo owner
still succeed (`enforce_admins: false`, a deliberate solo-maintainer gap, not a bug) but every
push now shows a "Bypassed rule violations" warning when it does. Prefer opening a PR for future
changes to actually exercise the merge policy Sprout itself now enforces, rather than relying on
the owner-bypass out of habit — same "don't take the easy path around your own invariant" spirit
as the rest of this file.
