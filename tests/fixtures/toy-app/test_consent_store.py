"""
Real RED->GREEN fixture for TASK-003 (docs/examples/ambient-journal/TASK-003.md):
"Revoke a granted signal's consent takes effect immediately." AC-003-02.

This is develop-next's TDD step run for real, not simulated, per M3's dogfood requirement.
"""
import unittest

from consent_store import ConsentStore, generate_draft


class TestConsentRevocationTakesEffectImmediately(unittest.TestCase):
    def test_revoked_signal_excluded_even_though_data_still_present(self):
        # AC-003-02: revoking a signal must exclude it from generation immediately, even if
        # signal data is still sitting right there in the input — this is the case a naive
        # "check consent once, cache the authorized list" implementation would get wrong.
        store = ConsentStore()
        store.grant("photo")
        store.grant("calendar")

        signals = {"photo": "a photo from today", "calendar": "lunch with a friend"}

        # revoke happens after data was already available, before generation runs
        store.revoke("photo")

        draft = generate_draft(store, signals)

        self.assertNotIn("photo", draft["signals_used"])
        self.assertIn("calendar", draft["signals_used"])

    def test_unrevoked_signals_still_included(self):
        store = ConsentStore()
        store.grant("photo")
        store.grant("calendar")

        draft = generate_draft(store, {"photo": "x", "calendar": "y"})

        self.assertIn("photo", draft["signals_used"])
        self.assertIn("calendar", draft["signals_used"])


if __name__ == "__main__":
    unittest.main()
