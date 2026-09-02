# Scenario: `/sprout:init` run against an already-initialized project

**Tests:** `skills/init/SKILL.md` — step 1.
**Failure mode being prevented:** a user with an existing Sprout project, wanting to bring it up
to date, runs the only command name they remember (`/sprout:init`) and gets a dead end — "already
initialized, stopping" with no indication that a different command exists for exactly what they
wanted. This is a real usability gap, not a hypothetical: it's the literal question a user asked
in this repo's own history before `skills/upgrade/SKILL.md` existed to answer it.

## Input

A repository with `.sprout/project.yaml` already present, on an older Sprout version than what's
currently installed. The user runs `/sprout:init`.

## Correct behavior

- `init` detects the project is already initialized and stops — it must not re-scaffold or
  silently start upgrading on its own (that's `upgrade`'s job, and it has its own ask-before-write
  discipline that `init` short-circuiting into it would bypass).
- The stop message names `/sprout:upgrade` specifically as the next step, not just "already
  initialized" with no forward path.

## Walkthrough against current skill

Step 1 now reads: "If already initialized, report current state and stop — do not re-scaffold.
Point at `/sprout:upgrade` instead..." — the dead end is closed without `init` taking on any of
`upgrade`'s responsibility itself.

**Gap check (pre-fix):** confirmed — the skill's prior text only said "report current state and
stop," with nothing telling the user what to do next. A user unfamiliar with the plugin's full
command surface would have no way to discover `/sprout:upgrade` from this interaction alone.

## Verdict

**RED → GREEN.** `init` now closes the exact gap a real user hit, without blurring the boundary
between "bootstrap a new project" and "bring an existing one up to date."
