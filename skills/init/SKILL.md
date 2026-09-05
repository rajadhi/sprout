---
name: init
description: Use when bootstrapping a repository for Sprout, or checking whether it already is — establishes .sprout/ control state and artifact directories without inventing product requirements or overwriting existing project artifacts
---

# init

## Overview

Bootstrap a downstream repository for Sprout use. This skill is pure scaffolding — it must not
invent product requirements, create tasks, commit unverified architecture decisions, or overwrite
existing project artifacts.

**Announce at start:** "I'm using the init skill to bootstrap Sprout for this project."

## Steps

1. **Detect repo state.** New or existing repository? Already Sprout-initialized (check for
   `.sprout/project.yaml`)? If already initialized, report current state and stop — do not
   re-scaffold. Point at `/sprout:upgrade` instead: that's the re-runnable path for bringing an
   already-initialized project's schema and tooling up to date with the currently installed
   plugin version, not this skill.
2. **Inspect the repository.** Read existing README, package manifests, CI config — infer what you
   can (platforms, stack) rather than asking for everything.
3. **Ask only for genuinely unresolved context**, from: project name, purpose, platforms,
   technology stack, repository, deployment environments, testing approach, accessibility target,
   security/privacy constraints, autonomy policy, production approval policy. Unknown values are
   allowed — write `unknown`, never invent one.
4. **Create the project profile** at `.sprout/project.yaml`, copied from
   `artifacts/project.yaml` in this plugin, filled with what you learned. Keep the shipped policy
   defaults (autonomy, task-sizing, verification, evidence, merge) unless the human overrides one.
   Set `sprout_version` to the installed plugin's actual `.claude-plugin/plugin.json` version —
   never leave the template's own `unknown` placeholder in place here; `/sprout:upgrade` reads
   this field to decide whether a later upgrade is even needed.
5. **Establish artifact directories** in the downstream repo:
   ```
   .sprout/{approvals,state,graph,runs}/
   thoughts/ requirements/ designs/ architecture/ tasks/ verification/ evidence/
   ```
6. **Establish project-specific Claude instructions** (a `CLAUDE.md` addendum) only if the project
   doesn't already have equivalent guidance.
7. **Establish GitHub conventions** — the `sprout:*` label set (type/state/risk/size), documented
   in `docs/architecture.md` of this plugin.
8. **Establish verification configuration** — confirm which check types (lint, unit, integration,
   ...) are available in this repo's toolchain; record in `project.yaml`.
9. **Offer to install merge enforcement**, not just artifact structure — scaffolding alone doesn't
   make `merge_policy` (`project.yaml`) a real property of this repo. Ask before copying (this
   writes into `.github/`, a repo-settings-adjacent area):
   - Copy this plugin's `.github/scripts/check_merge_readiness.py` into the downstream repo's
     `.github/scripts/`, and add a CI job that runs it on `pull_request` (see this plugin's own
     `.github/workflows/ci.yml` `merge-readiness-check` job for the exact shape — determine
     `BASE_SHA`/`HEAD_SHA`, pass the PR body through `env:` never inline into the shell, run the
     script). Deterministic, no API key or OAuth token, no network dependency — works from any
     tech stack since it only reads Sprout's own schema-defined artifact files, not the project's
     own toolchain. Offer the matching `tests/ci/test_check_merge_readiness.py` too, for the
     project's own regression coverage if they want it.
   - Offer a starter `CODEOWNERS` entry requiring review on the artifact directories from step 5
     (`requirements/ designs/ architecture/`, whichever risk-relevant ones apply).
   - Point at `docs/architecture.md` §7's GitHub-native settings checklist (branch protection
     required status checks, an R3/R4 approval Environment, secret scanning) as manual repo-admin
     steps this skill cannot perform itself.
10. **Report exactly what was created.** A flat list of files/directories, nothing implied — and
   which of step 9's offers were accepted vs. declined.

## Must not

- Invent product requirements
- Create arbitrary implementation tasks
- Commit unverified architecture decisions
- Overwrite existing project artifacts
