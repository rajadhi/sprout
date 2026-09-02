# Scenario: schema migration reports a blocked item — upgrade must not bump sprout_version anyway

**Tests:** `skills/upgrade/SKILL.md` — steps 3 and 6.
**Failure mode being prevented:** `upgrade` treating "I ran migrate" as "migration succeeded" and
writing the plugin's current version into `sprout_version` regardless of whether `migrate` itself
actually completed — the same unearned-advancement failure `docs/protocol.md` §1 forbids in
general, here specifically about a skill that delegates to another skill rather than doing the
work itself. It would be easy to treat delegation as automatically successful.

## Input

A project at `schema_version: 1`, plugin shipping `schema_version: 2`. `upgrade` delegates to
`/sprout:migrate` per step 3. `migrate` (see `docs/examples/schema-migration/MIGRATION.md` for the
exact real case this mirrors) completes two mechanical field transforms but reports one blocked
item — a new required field on a `RUN-*.md` with no derivable value — and, correctly per its own
step 7, does **not** bump `schema_version`.

## Correct behavior

- `upgrade` step 6 requires schema migration to have "completed" before writing
  `sprout_version` — a migration that finished with a reported blocker has not completed. Step 6
  is explicit: "Never bump this before every prior step has actually finished."
- The tooling backfill (step 4) still proceeds independently — schema and tooling are unrelated
  axes per step 3's own framing ("they're independent axes") — but the final report (step 8) must
  surface the blocked migration item explicitly, not bury it under a general "upgrade complete."
- `sprout_version` stays at whatever it was before this `upgrade` run; the project is left in a
  state where re-running `/sprout:upgrade` later (once a human resolves the blocked field) will
  pick the migration back up, the same way `migrate` itself is designed to be re-run after a
  blocker is cleared.

## Walkthrough against current skill

Step 3 requires waiting for `migrate` "to either complete or report a blocked item before
continuing" and requires the blocked case to be "reported alongside it, not silently dropped."
Step 6 ties the version bump explicitly to both schema migration *and* tooling backfill having
"actually finished." Step 8 requires the schema migration outcome to be reported as
"complete/blocked and why" — not folded into a generic success message.

**Gap check:** none found — the steps, read literally, block the premature version bump and
require the blocker to surface in the final report.

## Verdict

**GREEN.** Confirms `upgrade` inherits `migrate`'s own "don't claim a guarantee that isn't true
yet" discipline rather than laundering a partial success into an unqualified "upgraded."
