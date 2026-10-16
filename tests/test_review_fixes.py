"""Review-fix regression tests (final review fix pass, TDD)."""

import json
import stat
from pathlib import Path

import numpy as np
import pytest

import orchestrator as orch
from agents.cc import CcBackend
from targets.digital import flow as dflow


# --- Important 3: cc _coerce must not raise; bad-typed JSON falls back -------

FULL_KEYS = {"neurons": 1, "fanout": 2, "weight_width": 4, "timesteps": 8,
             "util_target": 60, "clock_ns": 4.0}
JOUR = [{"round": 0, "target": "digital", "config": dict(FULL_KEYS),
         "sim": {}, "flow": {}, "agent_note": ""}]


def _fake_claude(tmp_path: Path, out: str, exit_code: int = 0) -> None:
    bindir = tmp_path / "bin"
    bindir.mkdir(exist_ok=True)
    p = bindir / "claude"
    p.write_text(f"#!/bin/sh\nprintf '%s' '{out}'\nexit {exit_code}\n")
    p.chmod(p.stat().st_mode | stat.S_IEXEC | stat.S_IXGRP | stat.S_IXOTH)
    return bindir


def _cc(tmp_path, monkeypatch, out, exit_code=0):
    bindir = _fake_claude(tmp_path, out, exit_code)
    monkeypatch.setenv("PATH", str(bindir) + ":" + __import__("os").environ["PATH"])
    return CcBackend(journal_path=tmp_path / "j.jsonl", binary="claude", timeout_s=10)


def test_cc_null_value_falls_back_without_raising(tmp_path, monkeypatch):
    bad = dict(FULL_KEYS, neurons=None)
    b = _cc(tmp_path, monkeypatch, json.dumps(bad))
    assert b.propose_config(JOUR, "digital") == JOUR[-1]["config"]


def test_cc_uncoercible_string_falls_back(tmp_path, monkeypatch):
    bad = dict(FULL_KEYS, neurons="three hundred")
    b = _cc(tmp_path, monkeypatch, json.dumps(bad))
    assert b.propose_config(JOUR, "digital") == JOUR[-1]["config"]


def test_cc_clock_ns_string_coerced(tmp_path, monkeypatch):
    good = dict(FULL_KEYS, clock_ns="4.5")
    b = _cc(tmp_path, monkeypatch, json.dumps(good))
    cfg = b.propose_config(JOUR, "digital")
    assert cfg["clock_ns"] == 4.5


# --- Important 4: exceptions inside evaluate become verdicts, never escape ---

def test_evaluate_exception_becomes_fail_verdict(tmp_path, monkeypatch):
    class BoomTarget:
        name = "digital"
        DEFAULT_CFG = {}
        required_keys = ["x"]

        def evaluate(self, cfg, out_dir):
            raise RuntimeError("MemoryError-ish")

    monkeypatch.setattr(orch, "get_target", lambda name: BoomTarget())
    jp = orch.run_loop("digital", orch.StubBackend({"digital": [{"x": 1}, {"x": 2}]}),
                       rounds=2, out_root=tmp_path)
    recs = [json.loads(l) for l in jp.read_text().splitlines() if l.strip()]
    assert len(recs) == 2
    for r in recs:
        assert r["sim"]["verdict"] == "fail" and "MemoryError-ish" in r["sim"]["reason"]
        assert r["flow"] == {"verdict": "skipped", "reason": "sim failed"}


# --- Important 2: pipefail in docker cmd + stale results purged pre-run ------

def test_run_pnr_uses_pipefail_and_purges_stale_results(tmp_path, monkeypatch):
    orfs = tmp_path / "orfs"
    (orfs / "flow" / "designs" / "src").mkdir(parents=True)
    monkeypatch.setenv("ORFS_ROOT", str(orfs))
    stale = orfs / "flow" / "results" / dflow.PLATFORM / "snn_core_32" / "base"
    stale.mkdir(parents=True)
    (stale / "metadata.json").write_text('{"finish__timing__setup__ws": 0.5}')
    captured = {}

    def fake_run(cmd, **kw):
        captured["cmd"] = cmd
        class P:
            returncode = 1
            stdout = "boom"
        return P()

    monkeypatch.setattr(dflow.subprocess, "run", fake_run)
    monkeypatch.setattr(dflow.shutil, "which", lambda n: "/usr/bin/docker" if n == "docker" else None)
    m = dflow.run_pnr({"neurons": 32, "fanout": 4, "weight_width": 4,
                       "timesteps": 8, "util_target": 60, "clock_ns": 4.0},
                      tmp_path, timeout_s=10)
    assert m["verdict"] == "fail"  # stale metadata purged -> honest fail
    assert "pipefail" in captured["cmd"][-1]


# --- Minor 8: write_report survives flow:null --------------------------------

def test_report_survives_null_flow(tmp_path):
    from report.pareto import write_report
    jp = tmp_path / "j.jsonl"
    jp.write_text(json.dumps({"round": 0, "target": "digital", "config": {},
                              "sim": None, "flow": None, "agent_note": ""}) + "\n")
    out = write_report(jp, tmp_path / "r.md")
    assert out.exists()


# --- Minor 9: parse_metrics tolerates non-numeric metric strings -------------

def test_parse_metrics_non_numeric_skipped(tmp_path):
    d = tmp_path / "m"
    d.mkdir()
    (d / "metadata.json").write_text(json.dumps({
        "timing__setup__ws": "N/A",
        "timing__setup__ws__percent": 5.0,
        "power__total": "oops",
        "route__timing__setup__ws": 0.2,
    }))
    m = dflow.parse_metrics(d)
    assert m["verdict"] == "pass" and m["worst_slack_ns"] == 0.2
    assert m["pwr_w"] is None


# --- Minor 11: weight_width overflow warning ----------------------------------

def test_validate_warns_wide_weight_width():
    from common.config import REQUIRED_KEYS, validate_config
    cfg = dict(FULL_KEYS, neurons=512, weight_width=16)
    warns = validate_config("digital", cfg)
    assert any("weight_width" in w for w in warns)


# --- Minor 12: api CLI choice exits cleanly -----------------------------------

def test_cli_api_backend_clean_message(capsys, monkeypatch):
    import sys
    monkeypatch.setattr(sys, "argv",
                        ["orchestrator.py", "--target", "digital",
                         "--backend", "api", "--rounds", "1"])
    from orchestrator import main
    with pytest.raises(SystemExit) as e:
        main()
    assert e.value.code == 2
    assert "deferred" in capsys.readouterr().err


# --- Minor 6: weights docstring range — canonical helper ----------------------

def test_weight_range_signed_twos_complement():
    from targets.digital.model import weight_range
    assert weight_range(4) == (-8, 7)
    assert weight_range(8) == (-128, 127)