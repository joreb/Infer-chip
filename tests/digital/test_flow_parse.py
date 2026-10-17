"""parse_metrics / write_design / run_pnr fail-path tests (dockerless)."""

import json
from pathlib import Path

import pytest

from targets.digital.flow import parse_metrics, run_pnr, write_design

FIXTURE = Path(__file__).parent / "fixtures/orfs_reports"
CFG = {
    "neurons": 256, "fanout": 8, "weight_width": 4, "timesteps": 1024,
    "util_target": 60, "clock_ns": 4.0, "seed": 11,
}


def test_parse_metrics_from_metadata_fixture():
    m = parse_metrics(FIXTURE)
    assert m["verdict"] == "pass"
    assert isinstance(m["worst_slack_ns"], float) and m["worst_slack_ns"] == 0.1132
    assert isinstance(m["pwr_w"], float) and m["pwr_w"] == 4.24e-3
    assert isinstance(m["drc"], int) and m["drc"] == 0
    assert isinstance(m["area_mm2"], float) and abs(m["area_mm2"] - 31240.55 / 1e6) < 1e-12
    assert isinstance(m["wirelength_um"], float) and m["wirelength_um"] == 58400.72


def test_parse_metrics_missing_metadata_fails_soft():
    empty = FIXTURE.with_name("orfs_reports_empty")
    if not empty.exists():
        empty.mkdir()
    m = parse_metrics(empty)
    assert m["verdict"] == "fail" and m["reason"]


def test_write_design_creates_config_and_rtl(tmp_path):
    out = write_design(CFG, tmp_path)
    conf = (tmp_path / "orfs" / "config.mk").read_text()
    rtl = tmp_path / "orfs" / "snn_core.v"
    assert rtl.exists() and conf
    # DESIGN_NAME must equal the generated top module (real yosys rejects a
    # mismatch: "ERROR: Module `snn_core' not found!"), nickname names the
    # results dir
    assert "DESIGN_NAME = snn_core_256\n" in conf
    assert "DESIGN_NICKNAME = snn_core_256" in conf
    assert "sky130hs" in conf
    assert "CORE_UTILIZATION = 60" in conf
    assert "CLOCK_PERIOD = 4.0" in conf
    # get_ports must be Tcl-evaluated: ORFS copies the SDC verbatim to
    # 1_2_yosys.sdc and load_design read_sdc treats a braced argument as a
    # list of literal pin names ("pin '[get_ports' not found", STA-0132)
    sdc = (tmp_path / "orfs" / "snn_core.sdc").read_text()
    assert "create_clock -name clk -period 4.0 [get_ports clk]" in sdc
    assert "{[get_ports" not in sdc


def test_run_pnr_docker_missing_returns_fail_verdict(tmp_path, monkeypatch):
    import targets.digital.flow as flow
    monkeypatch.setattr(flow.shutil, "which", lambda name: None)
    m = flow.run_pnr(CFG, tmp_path, timeout_s=60)
    assert m["verdict"] == "fail" and "docker" in m["reason"].lower()