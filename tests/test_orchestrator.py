"""Orchestrator round-loop tests with fakes (no real sims)."""

import json  # noqa: F401  (used in journal-line assertions below)
import shutil  # noqa: F401  (module import guard parity)
from pathlib import Path

import pytest

import orchestrator as orch
from agents.stub import StubBackend


def _fail_target():
    class FailTarget:
        name = "digital"
        DEFAULT_CFG = {"dummy": True}

        def evaluate(self, cfg, out_dir):
            return {"sim": {"verdict": "fail", "reason": "sim died"},
                    "flow": {"verdict": "fail", "reason": "flow died"},
                    "config": cfg}

    return FailTarget()


def test_all_rounds_fail_journal_has_notes(tmp_path, monkeypatch):
    monkeypatch.setattr(orch, "get_target", lambda name: _fail_target())
    seq = {"digital": [{"cfg": i} for i in range(3)]}
    jp = orch.run_loop("digital", StubBackend(seq), rounds=3, out_root=tmp_path)
    lines = [l for l in jp.read_text().splitlines() if l.strip()]
    import json
    recs = [json.loads(l) for l in lines]
    assert len(recs) == 3
    for r in recs:
        assert r["flow"]["verdict"] == "fail"
        assert r["agent_note"]
        assert r["sim"]["verdict"] == "fail"
    assert jp.exists()


def test_backend_none_ends_loop(tmp_path, monkeypatch):
    monkeypatch.setattr(orch, "get_target", lambda name: _fail_target())
    seq = {"digital": [{"cfg": 0}]}  # one config then None
    jp = orch.run_loop("digital", StubBackend(seq), rounds=5, out_root=tmp_path)
    lines = [l for l in jp.read_text().splitlines() if l.strip()]
    assert len(lines) == 1


def test_ram_warning_proceeds(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(orch, "get_target", lambda name: _fail_target())
    seq = {"digital": [{"neurons": 10**9, "fanout": 10, "weight_width": 8,
                        "timesteps": 1000, "util_target": 60, "clock_ns": 4.0}]}
    jp = orch.run_loop("digital", StubBackend(seq), rounds=1, out_root=tmp_path)
    assert jp.exists()
    err = capsys.readouterr().err
    assert "memory" in err.lower()


def test_override_backfills_when_backend_proposes_none(tmp_path, monkeypatch):
    monkeypatch.setattr(orch, "get_target", lambda name: _fail_target())
    seed = StubBackend({})  # proposes None every round
    jp = orch.run_loop("digital", seed, rounds=3, out_root=tmp_path,
                       config_override={"neurons": 128, "fanout": 8,
                                        "weight_width": 4, "timesteps": 64,
                                        "util_target": 60, "clock_ns": 4.0})
    lines = [l for l in jp.read_text().splitlines() if l.strip()]
    assert len(lines) == 3  # override replays when backend has nothing


def test_invalid_proposals_fall_back_default_then_previous(tmp_path, monkeypatch):
    t = _fail_target()
    seen = []
    orig = t.evaluate

    def spy(cfg, out_dir):
        seen.append(cfg)
        return orig(cfg, out_dir)

    t.evaluate = spy
    monkeypatch.setattr(orch, "get_target", lambda name: t)
    seq = {"digital": [{"foo": 1}, {"bar": 2}]}  # both invalid for digital
    jp = orch.run_loop("digital", StubBackend(seq), rounds=2, out_root=tmp_path,
                       config_override={"from_override": 5})
    assert len(seen) == 2
    assert seen[0]["dummy"] is True and seen[0]["from_override"] == 5  # DEFAULT_CFG round 1
    assert seen[1]["dummy"] is True and seen[1]["from_override"] == 5  # keep previous
    assert "neurons" not in seen[0]


def test_concurrent_invocations_isolated_run_dirs_and_journal_lines(tmp_path, monkeypatch):
    """Two invocations on one out_root must not clobber each other (real
    defect: an orphaned duplicate orchestrator ran concurrently and both
    wrote into round_0, journal lines unattributable). Each invocation gets
    its own per-round subdir, and every journal line names its writer."""
    seen_dirs = []

    class SpyTarget:
        name = "digital"
        DEFAULT_CFG = {"dummy": True}

        def evaluate(self, cfg, out_dir):
            seen_dirs.append(Path(out_dir))
            return {"sim": {"verdict": "pass"}, "flow": {"verdict": "pass"}}

    class PassOnce:  # proposes None every round -> DEFAULT_CFG path
        def propose_config(self, journal, target):
            return None
        def analyze_failure(self, stage, logs, cfg):
            return ""

    monkeypatch.setattr(orch, "get_target", lambda name: SpyTarget())
    for _ in range(2):
        orch.run_loop("digital", PassOnce(), rounds=1, out_root=Path(tmp_path))
    recs = [json.loads(l) for l in
            (Path(tmp_path) / "digital" / "journal.jsonl").read_text().splitlines()
            if l.strip()]
    assert len(recs) == 2
    invs = [r["inv"] for r in recs]
    assert invs[0] != invs[1]                          # every line names its writer
    assert len(seen_dirs) == 2 and seen_dirs[0] != seen_dirs[1]
    # shared round dir, isolated per-invocation subdirs beneath it
    assert seen_dirs[0].parent == seen_dirs[1].parent