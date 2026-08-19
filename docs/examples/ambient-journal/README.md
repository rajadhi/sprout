# Ambient Journal — dogfooded shape + design + plan loop

This is not a spec to build Ambient Journal — it's M2 and M3's proof artifact, demonstrating
`docs/protocol.md`'s exit criteria with real files instead of a description of one. M2's:

> messy raw input becomes an approved, immutable requirement + design version; changing it
> produces a new version without touching history.

Every file here was produced by actually walking `skills/shape/SKILL.md`,
`skills/design/SKILL.md`, and `skills/plan/SKILL.md` against real input, including the fixes
those pressure scenarios (`tests/scenarios/`) surfaced.

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
8. **[APR-00003](APR-00003.md)** — approval for v2, including an impact-analysis note that
   `DES-001` needs a v2 too. **This note turned out to be wrong** — see step 10.
9. **plan decomposes REQ-001-v2/REQ-002/REQ-003 + DES-001** into 9 vertical-slice tasks
   (**[TASK-001](TASK-001.md)** through **[TASK-009](TASK-009.md)**), by user-visible behavior
   (consent per signal, empty state, draft generation, edit-persists) rather than technical layer.
   - Decomposition surfaced a real consequential decision — how the end-of-day trigger fires
     reliably on iOS — that wasn't covered by an existing ADR. Per `plan`'s rule 4, drafted
     **[ADR-001](ADR-001.md)** and dispatched `architecture-reviewer` before treating it as
     settled, approved as **[APR-00004](APR-00004.md)**. `TASK-005` implements the decision.
   - `plan`'s rule 9 ("mark `READY` only when prerequisites are satisfied") holds for real:
     **[TASK-009](TASK-009.md)** was originally marked `BLOCKED`, not `READY` — believed to need
     `DES-001-v2`. `TASK-006` (the backend enforcement half of the same v1→v2 fallout) has no such
     dependency and *is* `READY`.
10. **Re-running `/sprout:graph`'s impact analysis for real caught a mistake, not just confirmed
    one.** `APR-00003`'s note that `DES-001` "references location" was written by reasoning from
    the requirement diff, never actually checked against `DES-001-v1.md`'s real content. Grepping
    it (`grep -c -i location DES-001-v1.md` → `0`) shows it was written signal-agnostically and
    never needed updating. **[GRAPH-REQ-001](GRAPH-REQ-001.md)** has the full correction — and the
    correction itself had to route around `REQ-001-v2`/`APR-00003` being immutable
    (`hooks/check-immutable-artifacts.py` genuinely blocks editing them, confirmed by trying).
    Instead: **[TASK-009](TASK-009.md)** is now `RETIRED` — a new task state added specifically
    because "this task's premise turned out false" had no correct home in the original 12-state
    machine (`docs/protocol.md` §7) — with the original (wrong) planning rationale kept in the
    file, not erased, alongside the correction.
11. **[STATUS.md](STATUS.md)** — a real `/sprout:status` run reflecting the corrected state: 8
    ready, 0 blocked, 1 retired.

## What this proves

- Immutability held under real pressure: a genuine behavior change (dropping a signal) produced a
  new version, not a silent edit — `REQ-001-v1` is still readable, still shows what was approved
  and when, still marked with exactly why it's superseded.
- The granularity fix from M2's pressure testing actually changes shaped output — INT-0001 became
  3 requirements, not 1.
- The approval-gate fix actually changes what "ready for human approval" means — DES-001 shows its
  own pre-approval critic findings and their resolution, not just a clean final draft with no
  trace of the gate having done anything.
- `plan`'s dependency gate actually withholds `READY` when a real prerequisite is missing
  (`TASK-009`), rather than marking everything `READY` because it's been decomposed.
- The `architecture-reviewer` agent — wired into `plan` after M1 found it was unused — actually
  gets dispatched for a real consequential decision (`ADR-001`), not just referenced in docs.
- Dogfooding surfaced a real spec gap: the `checks:` enumeration never had a `security` value even
  though `evidence.md` has always had `SECURITY_RESULT` — found because `TASK-006` genuinely
  needed a security check. Fixed across `artifacts/project.yaml`, `artifacts/task.md`,
  `skills/verify/SKILL.md`, and `docs/protocol.md`.
- The immutability hook isn't decorative: when the fix for a real mistake required editing an
  approved requirement and its approval record, the hook actually said no (exit 2, confirmed by
  trying), and the correction had to go through the only legitimate path — a new artifact, not a
  quiet rewrite of history.
- `/sprout:graph`'s impact analysis can be wrong if it reasons from a diff instead of the actual
  downstream artifact — and re-running it for real, not just trusting the first pass, is what
  caught that. `skills/graph/SKILL.md` now says this explicitly, added because of this exact case.

## What this does not prove

This fixture does not yet exercise `develop-next` or `verify` against its own tasks for real — no
branch, no code, no verification run exists for any of these Ambient Journal tasks specifically
(`tests/fixtures/toy-app` is a separate, real proof of the develop-next+verify mechanics, modeled
on `TASK-003` but not literally executing it).
