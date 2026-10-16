"""Deterministic stub backend — scripted config sequences per target."""

from agents.base import Backend


class StubBackend(Backend):
    def __init__(self, sequences: dict[str, list[dict]] | None = None):
        self.sequences = {t: list(s) for t, s in (sequences or {}).items()}
        self._popped: dict[str, int] = {}

    def propose_config(self, journal_tail: list[dict], target: str) -> dict | None:
        i = self._popped.get(target, 0)
        seq = self.sequences.get(target, [])
        if i >= len(seq):
            return None
        self._popped[target] = i + 1
        return seq[i]

    def analyze_failure(self, stage: str, logs: str, cfg: dict) -> str:
        return f"stub-analysis: {stage} failed with cfg={cfg}; last-log={logs[-120:]!r}"