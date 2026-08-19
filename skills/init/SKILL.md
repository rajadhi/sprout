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
   re-scaffold.
2. **Inspect the repository.** Read existing README, package manifests, CI config — infer what you
   can (platforms, stack) rather than asking for everything.
3. **Ask only for genuinely unresolved context**, from: project name, purpose, platforms,
   technology stack, repository, deployment environments, testing approach, accessibility target,
   security/privacy constraints, autonomy policy, production approval policy. Unknown values are
   allowed — write `unknown`, never invent one.
4. **Create the project profile** at `.sprout/project.yaml`, copied from
   `artifacts/project.yaml` in this plugin, filled with what you learned. Keep the shipped policy
   defaults (autonomy, task-sizing, verification, evidence, merge) unless the human overrides one.
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
9. **Report exactly what was created.** A flat list of files/directories, nothing implied.

## Must not

- Invent product requirements
- Create arbitrary implementation tasks
- Commit unverified architecture decisions
- Overwrite existing project artifacts
