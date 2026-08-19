---
id: EVD-toy-001
type: UNIT_TEST_RESULT
verification_run: RUN-toy-001
task: TASK-003 (docs/examples/ambient-journal/TASK-003.md, AC-003-02)
commit: n/a — uncommitted fixture, see tests/fixtures/toy-app/README.md for the known
  simplification (no isolated branch/worktree was used for this fixture)
environment: "local, python3.9.6, stdlib unittest, no external dependencies"
timestamp: "2026-09-04"
source: "python3 -m unittest test_consent_store.py -v, run for real, not simulated"
description: >
  Real GREEN run after a real RED run (captured in tests/fixtures/toy-app/README.md). Proves
  AC-003-02: revoking a signal excludes it from generation immediately, even though the signal's
  data was still present in the input at generation time — the case a "cache the authorized list
  once" implementation would get wrong.
redaction_state: not_applicable
---

## Content

```
test_revoked_signal_excluded_even_though_data_still_present (test_consent_store.TestConsentRevocationTakesEffectImmediately) ... ok
test_unrevoked_signals_still_included (test_consent_store.TestConsentRevocationTakesEffectImmediately) ... ok

----------------------------------------------------------------------
Ran 2 tests in 0.000s

OK
```

Both tests pass: the revocation case (`test_revoked_signal_excluded_even_though_data_still_present`)
and the control case (`test_unrevoked_signals_still_included`), confirming the fix doesn't just
exclude everything — only what was actually revoked.
