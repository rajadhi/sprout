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


class TestDroppedLocationSignalNeverReadByGeneration(unittest.TestCase):
    def test_stale_cached_location_excluded_even_though_present_in_signals(self):
        # AC-001-04: location was dropped in the REQ-001 v1->v2 supersession. There is no
        # location consent path anymore, so it is never granted here. But stale/cached data
        # from a prior build could still show up in the signals dict passed to generate_draft
        # (e.g. leftover local storage from before the drop). Generation must not read or
        # reference it, even though it's sitting right there alongside signals that ARE granted.
        store = ConsentStore()
        store.grant("photo")
        store.grant("calendar")
        # location is deliberately never granted -- there's no such consent path per REQ-001-v2

        signals = {
            "photo": "x",
            "calendar": "y",
            "location": "stale cached location from a prior build",
        }

        draft = generate_draft(store, signals)

        self.assertNotIn("location", draft["signals_used"])
        self.assertIn("photo", draft["signals_used"])
        self.assertIn("calendar", draft["signals_used"])

    def test_location_excluded_even_if_somehow_granted_by_stale_data(self):
        # Defense in depth per AC-001-04: "the drop is enforced, not just unused going
        # forward." Even in the pathological case where stale prior-build data caused
        # "location" to be granted in the consent store, generation must still hard-block it --
        # it must not rely solely on the normal consent check.
        store = ConsentStore()
        store.grant("photo")
        store.grant("calendar")
        store.grant("location")  # simulates stale/corrupted consent state from a prior build

        signals = {
            "photo": "x",
            "calendar": "y",
            "location": "stale cached location from a prior build",
        }

        draft = generate_draft(store, signals)

        self.assertNotIn("location", draft["signals_used"])
        self.assertIn("photo", draft["signals_used"])
        self.assertIn("calendar", draft["signals_used"])


if __name__ == "__main__":
    unittest.main()
