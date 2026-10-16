"""Pareto front + markdown report tests."""

import json
import math
from pathlib import Path

from report.pareto import pareto_front, write_report

AXES = {"digital": ("area_mm2", "pwr_w")}


def test_pareto_front_only_nondominated():
    entries = [
        {"round": 0, "flow": {"area_mm2": 10.0, "pwr_w": 1.0}},
        {"round": 1, "flow": {"area_mm2": 20.0, "pwr_w": 2.0}},  # dominated
        {"round": 2, "flow": {"area_mm2": 20.0, "pwr_w": 0.5}},
    ]
    front = pareto_front(entries, "area_mm2", "pwr_w")
    assert sorted(e["round"] for e in front) == [0, 2]


def test_pareto_skips_nan_and_malformed():
    entries = [
        {"round": 0, "flow": {"area_mm2": 10.0, "pwr_w": 1.0}},
        {"round": 1, "flow": {"area_mm2": "not-a-number", "pwr_w": 1.0}},
        {"round": 2, "flow": {"area_mm2": math.nan, "pwr_w": 1.0}},
        {"round": 3, "flow": {"area_mm2": 10.0}},  # missing y
        {"round": 4},  # no flow at all
        {"round": 5, "flow": {"area_mm2": 5.0, "pwr_w": 5.0}},
        "garbage-line",
    ]
    for e in entries:
        if isinstance(e, dict):
            e.setdefault("target", "digital")
    front = pareto_front(entries, "area_mm2", "pwr_w")
    assert sorted(e["round"] for e in front) == [0, 5]


def test_write_report_headers_and_tables(tmp_path):
    jp = tmp_path / "journal.jsonl"
    recs = [
        {"round": 0, "target": "digital", "config": {"neurons": 256},
         "sim": {"verdict": "pass"}, "flow": {"verdict": "pass", "area_mm2": 0.03, "pwr_w": 4e-3},
         "agent_note": ""},
        {"round": 1, "target": "digital", "config": {"neurons": 512},
         "sim": {"verdict": "fail", "reason": "boom"}, "flow": {"verdict": "skipped"},
         "agent_note": "stub-analysis: sim failed"},
        {"round": 0, "target": "photonic", "config": {"mesh_depth": 4},
         "sim": {"verdict": "pass"}, "flow": {"verdict": "pass", "footprint_mm2": 0.02, "energy_per_mac_pj": 0.8},
         "agent_note": ""},
    ]
    jp.write_text("\n".join(json.dumps(r) for r in recs) + "\n")
    out_md = tmp_path / "report.md"
    result = write_report(jp, out_md)
    assert result == out_md
    md = out_md.read_text()
    for header in ("## digital", "## photonic"):
        assert header in md
    assert "0.03" in md and "stub-analysis" in md and "boom" in md
    # malformed journal line doesn't crash
    with open(jp, "a") as f:
        f.write("garbage\n")
    write_report(jp, tmp_path / "report2.md")