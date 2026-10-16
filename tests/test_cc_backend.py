"""CcBackend shellout tests — fake `claude` binaries via monkeypatched PATH."""

import json
import stat
from pathlib import Path

import pytest

from agents.cc import CcBackend
from common.config import REQUIRED_KEYS

JOUR = [
    {"round": 0, "target": "digital", "config": {"neurons": 32}, "sim": {}, "flow": {}, "agent_note": ""},
    {"round": 1, "target": "digital", "config": {"neurons": 64}, "sim": {}, "flow": {}, "agent_note": ""},
]


def _fake_bin(tmp_path: Path, name: str, code: str) -> str:
    bindir = tmp_path / "bin"
    bindir.mkdir(exist_ok=True)
    p = bindir / name
    p.write_text("#!/bin/sh\n" + code)
    p.chmod(p.stat().st_mode | stat.S_IEXEC | stat.S_IXGRP | stat.S_IXOTH)
    return str(bindir)


FULL_CFG = {"neurons": 128, "fanout": 8, "weight_width": 4, "timesteps": 64,
            "util_target": 60, "clock_ns": 4.0}


def test_propose_parses_last_json(tmp_path, monkeypatch):
    payload = dict(FULL_CFG, neurons="512", fanout=8)
    bindir = _fake_bin(
        tmp_path, "claude",
        "echo 'noise\\n" + json.dumps(payload).replace("'", "'\\''") + "'")
    monkeypatch.setenv("PATH", str(bindir) + ":" + __import__("os").environ["PATH"])
    b = CcBackend(journal_path=tmp_path / "j.jsonl", binary="claude", timeout_s=10)
    cfg = b.propose_config(JOUR, "digital")
    assert cfg is not None
    assert cfg["neurons"] == 512  # str coerced to int per REQUIRED_KEYS types
    assert cfg["fanout"] == 8


def test_propose_non_json_falls_back_to_prev_config(tmp_path, monkeypatch):
    bindir = _fake_bin(tmp_path, "claude", 'echo abc')
    monkeypatch.setenv("PATH", str(bindir) + ":" + __import__("os").environ["PATH"])
    b = CcBackend(journal_path=tmp_path / "j.jsonl", binary="claude", timeout_s=10)
    cfg = b.propose_config(JOUR, "digital")
    assert cfg == JOUR[-1]["config"]


def test_propose_exit_3_also_falls_back(tmp_path, monkeypatch):
    bindir = _fake_bin(tmp_path, "claude", 'exit 3')
    monkeypatch.setenv("PATH", str(bindir) + ":" + __import__("os").environ["PATH"])
    b = CcBackend(journal_path=tmp_path / "j.jsonl", binary="claude", timeout_s=10)
    cfg = b.propose_config(JOUR, "digital")
    assert cfg == JOUR[-1]["config"]


def test_propose_no_history_no_json_returns_none(tmp_path, monkeypatch):
    bindir = _fake_bin(tmp_path, "claude", 'echo "garbage"')
    monkeypatch.setenv("PATH", str(bindir) + ":" + __import__("os").environ["PATH"])
    b = CcBackend(journal_path=tmp_path / "j.jsonl", binary="claude", timeout_s=10)
    assert b.propose_config([], "digital") is None


def test_analyze_failure_raw_text(tmp_path, monkeypatch):
    bindir = _fake_bin(tmp_path, "claude", 'echo "check timing slack"')
    monkeypatch.setenv("PATH", str(bindir) + ":" + __import__("os").environ["PATH"])
    b = CcBackend(journal_path=tmp_path / "j.jsonl", binary="claude", timeout_s=10)
    assert b.analyze_failure("flow", "setup violated", {}) == "check timing slack"


def test_analyze_failure_unparseable(tmp_path, monkeypatch):
    bindir = _fake_bin(tmp_path, "claude", 'exit 1')
    monkeypatch.setenv("PATH", str(bindir) + ":" + __import__("os").environ["PATH"])
    b = CcBackend(journal_path=tmp_path / "j.jsonl", binary="claude", timeout_s=10)
    assert b.analyze_failure("flow", "x", {}) == "no analysis"


def test_prompt_carries_required_keys(tmp_path, monkeypatch):
    bindir = tmp_path / "bin"
    bindir.mkdir(exist_ok=True)
    cap = bindir / "args.txt"
    p = bindir / "claude"
    p.write_text('#!/bin/sh\necho "$@" > "$CAPTURE_FILE"\necho \''
                 + json.dumps(FULL_CFG).replace("'", "'\\''") + '\'\n')
    p.chmod(p.stat().st_mode | stat.S_IEXEC | stat.S_IXGRP | stat.S_IXOTH)
    monkeypatch.setenv("PATH", str(bindir) + ":" + __import__("os").environ["PATH"])
    monkeypatch.setenv("CAPTURE_FILE", str(cap))
    b = CcBackend(journal_path=tmp_path / "j.jsonl", binary="claude", timeout_s=10)
    cfg = b.propose_config([], "digital")
    assert cfg == FULL_CFG
    prompt = cap.read_text()
    for k in REQUIRED_KEYS["digital"]:
        assert k in prompt