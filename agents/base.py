"""Agent backend contract: target-agnostic config proposer + failure analyst."""

from typing import Protocol, runtime_checkable


@runtime_checkable
class Backend(Protocol):
    def propose_config(self, journal_tail: list[dict], target: str) -> dict | None:
        """Next config to try for this target, or None to stop the loop."""
        ...

    def analyze_failure(self, stage: str, logs: str, cfg: dict) -> str:
        """One-paragraph diagnosis for the journal's agent_note."""
        ...


def get_backend(name: str, **kw):
    if name == "stub":
        from agents.stub import StubBackend
        return StubBackend(**kw)
    if name == "cc":
        from agents.cc import CcBackend
        return CcBackend(**kw)
    if name == "api":
        raise KeyError(f"{name!r} backend deferred to stage-1")
    raise KeyError(f"unknown backend: {name!r} (stub|cc)")