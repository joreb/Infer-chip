"""Agent backend contract + stub tests."""

import pytest

from agents.base import get_backend
from agents.stub import StubBackend


def test_stub_pops_in_order_then_none():
    seq = {
        "digital": [{"neurons": 32}, {"neurons": 64}],
        "photonic": [{"mesh_depth": 4}],
    }
    b = StubBackend(seq)
    assert b.propose_config([], "digital") == {"neurons": 32}
    assert b.propose_config([], "digital") == {"neurons": 64}
    assert b.propose_config([], "digital") is None
    assert b.propose_config([], "photonic") == {"mesh_depth": 4}
    assert b.propose_config([], "memristive") is None  # no sequence


def test_analyze_failure_returns_note():
    b = StubBackend({})
    note = b.analyze_failure("flow", "error log lines", {"neurons": 32})
    assert isinstance(note, str) and note


def test_get_backend_registry():
    assert isinstance(get_backend("stub"), StubBackend)
    with pytest.raises(KeyError, match="deferred"):
        get_backend("api")
    with pytest.raises(KeyError):
        get_backend("nope")