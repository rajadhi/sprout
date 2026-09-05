# Dogfood: `/sprout:migrate` against a synthetic schema_version 1 -> 2 transition

A synthetic fixture, not a real Sprout schema change — `artifacts/project.yaml`'s real
`schema_version` stays `1` (see `docs/protocol.md`). This exercises `skills/migrate/SKILL.md`'s
actual steps against a made-up but realistic v2 schema, the same way `tests/fixtures/toy-app` is
real code without being part of Sprout's own application. `before/` and `after/` are both real
files, actually produced by walking the skill's steps — not a narrative of what would happen.

## The synthetic v2 schema

Three changes, chosen to exercise three different code paths in `migrate`'s steps 5-6:

1. **`TASK-*.md`: `implements:` refs must pin a version** (`[REQ-XXX]` → `[REQ-XXX@vN]`) —
   mechanically derivable (point at whatever version is currently approved) and on an unversioned
   artifact type, so migrate updates in place. This is also a real gap named in the external
   v0.2.0 review ("task edges use `implements: [REQ-XXX]` without the version... reliable
   staleness detection impossible") — using it here means this fixture is exercising a migration
   this project may plausibly need for real one day, not a contrived example.
2. **`TASK-*.md`: new `claimed_by:` field** — mechanically derivable (always `null` at migration
   time; nothing was claimed under v1, the field didn't exist), unversioned type, update in place.
3. **`REQ-*.md`: `type:` renamed to `category:`** — mechanically derivable (straight rename,
   value unchanged), but `REQ-100` v1 is `APPROVED` — immutable in place per `docs/protocol.md`
   §1.5 — so this one *must* produce `REQ-100` v2 instead of editing v1's frontmatter, testing
   step 6's versioned-type branch for real.
4. **`RUN-*.md`: new required `verification_environment:` field** — deliberately **not**
   mechanically derivable (there's no way to know what environment `RUN-00100` actually ran in
   from data that exists today) — this is the case step 5 says migrate must stop and ask a human
   for, tested here by confirming it actually does stop rather than guessing `unknown` or
   inventing a plausible-sounding value.

## Walkthrough against `skills/migrate/SKILL.md`

1. Read `before/project.yaml`'s `schema_version`: `1`.
2. Target: `2` (the synthetic version this fixture is migrating toward).
3. They don't match — proceed.
4. Artifact types whose schema changed: `TASK-*.md` (two changes), `REQ-*.md` (one change).
   `RUN-*.md` also changed (one change) — included below. Nothing else in this fixture's schema
   changed, so nothing else is touched.
5. Field-level transforms:
   - `TASK-100.implements`: `[REQ-100]` → `[REQ-100@v2]` — derived from the requirement's current
     approved version at migration time, not guessed.
   - `TASK-100.claimed_by`: added as `null` — the only correct default; nothing could have been
     claimed under a schema that didn't have the field.
   - `REQ-100.type` → `REQ-100.category`: straight rename, value (`engineering`) preserved.
   - `RUN-100.verification_environment`: **no derivable value exists.** Per step 5, migrate stops
     here rather than inventing one (`unknown`, `production`, or any other guess would be exactly
     the fabrication `docs/protocol.md` forbids). This is a genuine, unresolved blocker — recorded
     below, not swept under a default.
6. Writing the changes:
   - `TASK-100.md` (unversioned type) — updated in place. See `after/TASK-100.md`.
   - `REQ-100` (versioned, immutable once `APPROVED`) — `before/REQ-100-v1.md` is **not** edited
     in place. Instead: `after/REQ-100-v1.md` gets only `status: SUPERSEDED` and
     `superseded_by: REQ-100 v2` changed (both in the hook's allowed-field set,
     `hooks/check-immutable-artifacts.py`'s `ALLOWED_FIELDS` — body untouched), and
     `after/REQ-100-v2.md` is a new file carrying the migrated `category:` field and
     `supersedes: REQ-100 v1`.
   - `RUN-00100.md` — **left untouched.** `after/RUN-00100.md` is byte-identical to
     `before/RUN-00100.md`. Blocked, not migrated.
7. `schema_version` bump: **not performed.** `after/project.yaml` still reads
   `schema_version: 1`, exactly as step 7 requires ("only after every affected artifact has
   migrated successfully") — `RUN-00100` never migrated, so the project-wide version cannot
   advance. A migration that "mostly" succeeded and bumped the version anyway would silently claim
   a guarantee (every v1 artifact is now v2-shaped) that isn't true.
8. Report:
   - Migrated: `TASK-100.md` (2 fields), `REQ-100` (new v2 created, v1 marked superseded).
   - Unchanged: nothing else in this fixture's schema surface.
   - **Needs a human decision:** `RUN-00100.md` needs a `verification_environment` value that
     can't be derived from existing data — someone who knows what environment that run actually
     executed in has to supply it before this migration can complete and `schema_version` can
     advance to `2`.

## Verdict

**GREEN**, with one deliberate, honestly-reported incompleteness. `migrate`'s steps, applied
literally to a case with a real non-derivable field, produce exactly the behavior the skill
promises: real transforms where they're mechanical, a stop-and-ask where they're not, and no
premature version bump. Confirms this isn't just well-worded — the "never guess a value" rule
actually changes what gets written when tested against a field that has no honest default.
