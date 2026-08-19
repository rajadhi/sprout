"""
Minimal implementation for TASK-003 (docs/examples/ambient-journal/TASK-003.md).
Deliberately small — just enough to satisfy test_consent_store.py's AC-003-02 cases.
"""


class ConsentStore:
    def __init__(self):
        self._granted = set()

    def grant(self, signal):
        self._granted.add(signal)

    def revoke(self, signal):
        self._granted.discard(signal)

    def is_granted(self, signal):
        return signal in self._granted


def generate_draft(store: ConsentStore, signals: dict) -> dict:
    # Checks consent at generation time, not at some earlier cached point — this is what makes
    # revocation take effect immediately (AC-003-02) rather than only affecting future signal
    # reads.
    used = {name: value for name, value in signals.items() if store.is_granted(name)}
    return {"signals_used": used}
