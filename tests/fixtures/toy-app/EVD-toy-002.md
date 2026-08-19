---
id: EVD-toy-002
type: UNIT_TEST_RESULT
verification_run: RUN-toy-002
task: TASK-006 (docs/examples/ambient-journal/TASK-006.md, AC-001-04)
commit: 8cff5aaa182763de50a55bdb8d818825c15b7064
environment: "local, python3.9.6, stdlib unittest, no external dependencies"
timestamp: "2026-08-19"
source: "python3 -m unittest test_consent_store.py -v, run for real in a git worktree (branch task-006-enforce-dropped-signal), implemented by a dispatched subagent per Superpowers' test-driven-development skill"
description: >
  Real GREEN run proving AC-001-04: the location signal, dropped in the REQ-001 v1->v2
  supersession, is never read by generation even if stale data or a stale/corrupted consent
  grant makes it present. The literal originally-imagined scenario (location never granted, data
  merely present) already passed under the pre-existing consent check alone -- not a real RED
  test. The adversarial case (location somehow granted by stale prior-build state) produced a
  genuine failure against the old implementation, fixed with an explicit denylist. Both cases now
  pass.
redaction_state: not_applicable
---

## Content

```
test_revoked_signal_excluded_even_though_data_still_present (test_consent_store.TestConsentRevocationTakesEffectImmediately) ... ok
test_unrevoked_signals_still_included (test_consent_store.TestConsentRevocationTakesEffectImmediately) ... ok
test_location_excluded_even_if_somehow_granted_by_stale_data (test_consent_store.TestDroppedLocationSignalNeverReadByGeneration) ... ok
test_stale_cached_location_excluded_even_though_present_in_signals (test_consent_store.TestDroppedLocationSignalNeverReadByGeneration) ... ok

----------------------------------------------------------------------
Ran 4 tests in 0.000s

OK
```

Real RED, captured before the fix (`git show 8cff5aaa -- tests/fixtures/toy-app/consent_store.py`
for the diff that turned this red test green):

```
test_location_excluded_even_if_somehow_granted_by_stale_data ... FAIL
AssertionError: 'location' unexpectedly found in {'photo': 'x', 'calendar': 'y', 'location': 'stale cached location from a prior build'}
Ran 4 tests in 0.000s
FAILED (failures=1)
```
