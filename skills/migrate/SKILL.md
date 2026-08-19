---
name: migrate
description: Use when Sprout's own schema_version changes and existing artifacts in a downstream project need to move to the new schema — never silently reinterprets old artifacts, always preserves the pre-migration version
---

# migrate

## Overview

Sprout's artifact schemas are versioned (`schema_version:` field, `artifacts/project.yaml` and
every artifact template). When Sprout itself changes a schema in a backward-incompatible way
(new required field, renamed field, changed meaning of an existing field), downstream projects
running an older `schema_version` need an explicit migration — never a silent reinterpretation.

**Announce at start:** "I'm using the migrate skill to move this project from schema_version <N>
to <N+1>."

## Steps

1. Read the project's current `schema_version` from `.sprout/project.yaml`.
2. Read Sprout's target `schema_version` (the plugin version being installed/updated to).
3. If they already match, report "already current" and stop.
4. Identify every artifact type whose schema actually changed between the two versions — not
   every artifact needs touching just because the project-wide version number moved.
5. For each affected artifact, apply the specific field-level transform (add a new field with an
   explicit default, rename a field preserving the old value, etc.) — never guess a value for a
   genuinely new required field; if it can't be derived mechanically from existing data, stop and
   ask the human.
6. Write the migrated content as a **new version of the artifact where the artifact type is
   itself versioned** (requirement/design/decision) — migration is a content change, and those
   types are immutable once approved, so migrating an approved one means creating the next
   version, not overwriting it. For unversioned types (tasks, project.yaml), update in place —
   these aren't in the immutable-artifact list (`docs/protocol.md` §1.5).
7. Bump `schema_version` in `.sprout/project.yaml` only after every affected artifact has
   migrated successfully.
8. Report exactly what was migrated, what stayed the same, and any items that needed a human
   decision.

## Must not

- Silently reinterpret an old-schema artifact as if it were already new-schema
- Migrate an artifact type whose schema didn't actually change
- Guess a value for a new required field that can't be mechanically derived
- Overwrite an approved requirement/design/decision in place instead of creating a new version
- Bump `schema_version` before every affected artifact has actually migrated
