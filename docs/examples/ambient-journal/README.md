# Ambient Journal — dogfooded shape + design loop

This is not a spec to build Ambient Journal — it's M2's proof artifact, demonstrating
`docs/protocol.md`'s M2 exit criterion with real files instead of a description of one:

> messy raw input becomes an approved, immutable requirement + design version; changing it
> produces a new version without touching history.

Every file here was produced by actually walking `skills/shape/SKILL.md` and
`skills/design/SKILL.md` against a real input, including the fixes those pressure scenarios
(`tests/scenarios/shape/`, `tests/scenarios/design/`) surfaced.

## Walkthrough

1. **[INT-0001](INT-0001.md)** — raw, messy human input. Bundles four distinct outcomes.
2. **shape splits it** per the granularity rule (`tests/scenarios/shape/huge-feature.md`) into
   three independent requirements: **[REQ-001-v1](REQ-001-v1.md)** (journal generation),
   **[REQ-002-v1](REQ-002-v1.md)** (user correction), **[REQ-003-v1](REQ-003-v1.md)** (per-signal
   consent) — each separately approvable.
3. **[APR-00001](APR-00001.md)** — immutable approval record for all three. Not chat history.
4. **design produces [DES-001-v1](DES-001-v1.md)** covering all three requirements' UX. First
   critic pass found 3 findings (recorded in the file's HTML comment); revision resolved them;
   second pass was clean — matches the approval-gate fix from
   `tests/scenarios/design/unresolved-criterion.md` (zero *open* findings required, not just "a
   critique pass happened").
5. **[APR-00002](APR-00002.md)** — immutable approval for the design.
6. **[INT-0002](INT-0002.md)** — a later, unrelated raw input: tester feedback that location feels
   invasive. This is where immutability gets tested for real.
7. **shape classifies this as SUPERSESSION**, not refinement — dropping a signal changes intended
   behavior. **[REQ-001-v2](REQ-001-v2.md)** is a *new file*, not an edit:
   - `REQ-001-v1.md`'s body is untouched. Only its `status` field moved to `SUPERSEDED` — a
     state-machine transition, not a content rewrite.
   - `v1` and `v2` cross-reference via `supersedes` / `superseded_by`.
   - v2 adds `AC-001-04` (enforce the drop, don't just stop using it) rather than silently
     deleting the location-related acceptance criteria from history.
8. **[APR-00003](APR-00003.md)** — approval for v2, including the impact-analysis note that
   `DES-001` needs a v2 too (`NEEDS_REVIEW`, not `INVALIDATED` — the flow structure holds, only
   the location-specific consent prompt needs removal). That next design version isn't included
   here — it's the natural next step, left undone on purpose so this fixture stays a proof of the
   shape→design→supersession loop, not a full Ambient Journal build.

## What this proves

- Immutability held under real pressure: a genuine behavior change (dropping a signal) produced a
  new version, not a silent edit — `REQ-001-v1` is still readable, still shows what was approved
  and when, still marked with exactly why it's superseded.
- The granularity fix from M2's pressure testing actually changes shaped output — INT-0001 became
  3 requirements, not 1.
- The approval-gate fix actually changes what "ready for human approval" means — DES-001 shows its
  own pre-approval critic findings and their resolution, not just a clean final draft with no
  trace of the gate having done anything.

## What this does not prove

This fixture does not exercise `plan`, `develop-next`, or `verify` — those are M3. No tasks, no
code, no verification runs exist for Ambient Journal yet, and shouldn't until M3 starts.
