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

M1 and M2 done (see `README.md` Status). Next is M3 (`plan → develop-next → verify`, integrated
with Superpowers) per `docs/protocol.md` §9. Do not jump ahead to M4 (GitHub Actions, branch
protection) until M3's exit criterion is met: a task cannot reach `VERIFIED` without a valid
evidence bundle, proven the same way M2 was — pressure scenarios plus a real dogfooded fixture,
not just a description of intended behavior.
