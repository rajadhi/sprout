---
name: upgrade
description: Use when bringing an already-initialized project's Sprout installation up to date with the latest installed plugin version — schema migration via migrate, enforcement tooling backfill (CI script, CODEOWNERS, settings checklist), and a doctor audit. The re-runnable counterpart to init for a project that's already Sprout-initialized.
---

# upgrade

## Overview

`init` only runs once — it stops immediately if `.sprout/project.yaml` already exists
(`skills/init/SKILL.md` step 1). But the plugin keeps moving: schema changes, new CI enforcement
scripts, new skill checks. A project initialized months ago has no path back to current except
manually diffing against the plugin's shipped files. `upgrade` is that path — the re-runnable
counterpart to `init`, combining three things that already exist rather than reimplementing any
of them: `migrate` for schema, a tooling diff-and-offer for everything `init` step 9 would have
installed on a fresh project, and `doctor` for a final audit.

**Announce at start:** "I'm using the upgrade skill to bring this project's Sprout installation up
to date."

## Steps

1. **Confirm this project is already initialized.** No `.sprout/project.yaml` → stop and point at
   `/sprout:init` instead; this skill has nothing to upgrade.
2. **Compare versions.** Read the project's `.sprout/project.yaml` `sprout_version` field against
   the installed plugin's `.claude-plugin/plugin.json` `version`. If they already match, and the
   project's `schema_version` also matches the plugin's shipped `artifacts/project.yaml`, report
   "already current" and stop — same discipline `migrate` step 3 uses for `schema_version` alone.
3. **Schema migration.** If `schema_version` differs, delegate to `/sprout:migrate` in full —
   don't reimplement its field-transform logic here. Wait for it to either complete or report a
   blocked item before continuing; a blocked migration doesn't prevent the tooling backfill below
   (they're independent axes: one is artifact shape, the other is CI/enforcement tooling), but
   must be reported alongside it, not silently dropped.
4. **Tooling backfill.** Diff the project's `.github/` against what the installed plugin currently
   ships:
   - `.github/scripts/check_merge_readiness.py` (and its regression test)
   - the `merge-readiness-check` job shape in `.github/workflows/ci.yml`
   - `CODEOWNERS`
   - any other deterministic check under the plugin's `.github/scripts/` the project doesn't have
     yet
   For each missing file: offer to add it (ask first — this writes into `.github/`, same
   discipline as `init` step 9). For each file that exists but differs from the plugin's shipped
   version: show the diff and ask whether to update or leave as-is — never silently overwrite a
   project's intentional customization. Never delete a project-specific script that isn't part of
   the plugin's shipped set, even if it looks similar to one that is.
5. **Point at the settings checklist.** `docs/architecture.md` §7's GitHub-native settings
   checklist (branch protection required checks, an R3/R4 Environment, secret scanning, Code
   Owners review requirement) — these are repo-admin actions no skill can perform. List which ones
   this project's current GitHub state already appears to satisfy (when `gh` access allows
   checking) and which don't, the same as `init` step 9 already points at this checklist rather
   than attempting the settings changes itself.
6. **Update the version markers.** Once schema migration (if any) has completed and every tooling
   offer from step 4 has been accepted or explicitly declined, write the plugin's current version
   into `.sprout/project.yaml`'s `sprout_version` field. Never bump this before every prior step
   has actually finished — the same "don't claim a guarantee that isn't true yet" discipline
   `migrate` step 7 applies to `schema_version`.
7. **Run `/sprout:doctor`** as a final audit of the resulting state — don't reimplement its checks
   here either.
8. **Report exactly what changed**: schema migration outcome (complete/blocked and why), each
   tooling item added/updated/declined/already-current, settings-checklist status, and `doctor`'s
   findings. A report that only says "upgraded" without this breakdown would repeat exactly the
   false-assurance problem `init` step 9/10 already exists to avoid.

## Must not

- Reimplement `migrate`'s field-transform logic, `doctor`'s checks, or `init` step 9's install
  logic instead of delegating to them
- Overwrite a project's customized version of a shipped file without showing the diff and asking
- Delete a project-specific script that isn't part of the plugin's shipped set
- Bump `sprout_version` before schema migration and tooling backfill have actually finished
- Attempt to change repo settings (branch protection, Environments, secret scanning) directly —
  list them as manual steps, the same as `init` step 9 already does
