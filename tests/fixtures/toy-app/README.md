# Toy app — real TDD → verify → evidence proof

M3's exit criterion (`docs/protocol.md` §9): *"a task cannot reach `VERIFIED` without a valid
evidence bundle."* M2 and the `plan` half of M3 proved their exit criteria with real markdown
artifacts but simulated behavior. This fixture instead runs real code, for real, to prove
`develop-next`'s TDD step and `verify`'s evidence-gating actually work — not just read well.

Modeled on `docs/examples/ambient-journal/TASK-003.md` (revoke a granted signal's consent takes
effect immediately, AC-003-02) — small enough to implement as pure logic with zero external
dependencies (stdlib `unittest`, no app framework, no network).

## What actually happened, in order

**1. RED** — wrote `test_consent_store.py` first, ran it before any implementation existed:

```
$ python3 -m unittest test_consent_store.py -v
ERROR: test_consent_store (unittest.loader._FailedTest)
ModuleNotFoundError: No module named 'consent_store'
Ran 1 test in 0.000s
FAILED (errors=1)
```

Real failure, not a described one — `consent_store.py` didn't exist yet.

**2. GREEN** — wrote the minimal `consent_store.py` needed to satisfy the test (see the file —
`ConsentStore.grant/revoke/is_granted` plus `generate_draft`, which checks consent *at generation
time* rather than caching an authorized-signals list earlier, which is exactly what AC-003-02
requires). Ran the suite again:

```
$ python3 -m unittest test_consent_store.py -v
test_revoked_signal_excluded_even_though_data_still_present ... ok
test_unrevoked_signals_still_included ... ok
Ran 2 tests in 0.000s
OK
```

Real pass — captured verbatim as **[EVD-toy-001](EVD-toy-001.md)**.

**3. Verify** — **[RUN-toy-001](RUN-toy-001.md)** applies `agents/verifier.md`'s actual steps: read
the acceptance criterion directly, check the evidence maps to it (not just "tests are green"),
apply the missing-evidence and commit-identity rules from `tests/scenarios/verify/`. Verdict:
`PASS`.

## Known simplification

Per the scope decision for this fixture: no isolated git worktree/branch was created (skipped
`develop-next`'s `CREATE ISOLATED WORKTREE/BRANCH` step), so `RUN-toy-001`'s `commit`/`branch_pr`
fields are `n/a` rather than real values. Everything else — RED, GREEN, evidence capture,
independent verdict reasoning against the acceptance criterion — is real. A production run of
`develop-next` would create the branch first; this fixture proves the TDD-and-evidence mechanics
that branch would contain, without the git ceremony around it.

## What this proves for M3

- `develop-next`'s TDD policy is executable, not just describable: a real RED test failed for a
  real reason (missing module), a real minimal implementation turned it GREEN.
- `verify`'s evidence-sufficiency bar holds against real command output, not a hypothetical one —
  the captured evidence is the actual terminal output, not a paraphrase of what it might show.
- The gap fixes from `tests/scenarios/verify/` (missing-evidence = automatic fail, commit-identity
  matters) are referenced and applied in `RUN-toy-001`'s reasoning against a real case, confirming
  they're usable in practice, not just correct as written.
