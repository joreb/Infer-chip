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


def _fake_docker(tmp_path, monkeypatch, run_impl):
    """Patch docker presence + subprocess.run; return the list of calls."""
    import targets.digital.flow as flow
    monkeypatch.setattr(flow.shutil, "which", lambda name: "/usr/bin/docker")
    calls = []

    def fake_run(cmd, **kw):
        calls.append(cmd)
        return run_impl(cmd, **kw)

    monkeypatch.setattr(flow.subprocess, "run", fake_run)
    return flow, calls


def test_run_pnr_generates_metadata_and_copies_reports_and_logs(tmp_path, monkeypatch):
    # bare `make` never runs genMetrics; ORFS writes metadata.json only from
    # `make metadata-generate`, into flow/reports/, not flow/results/ (#1)
    import subprocess
    ok = lambda cmd, **kw: subprocess.CompletedProcess(cmd, 0, "", "")
    flow, calls = _fake_docker(tmp_path, monkeypatch, ok)
    flow.run_pnr(CFG, tmp_path, timeout_s=60)
    docker_cmd = calls[0]
    sh = docker_cmd[-1]
    assert "metadata-generate" in sh
    assert "reports/sky130hs/snn_core_256" in sh
    assert "logs/sky130hs/snn_core_256" in sh
    assert "metadata.json" in sh
    # the run is reproducible from the record: full command saved on host
    assert (tmp_path / "docker_cmd.txt").read_text().strip().startswith("docker run")
    assert "--name" in docker_cmd


def test_run_pnr_timeout_kills_named_container_and_does_not_retry(tmp_path, monkeypatch):
    # subprocess timeout kills the docker CLI only; the container keeps
    # running, and a retry would start a second ORFS run beside it
    import subprocess

    def run_impl(cmd, **kw):
        if cmd[:2] == ["docker", "run"]:
            raise subprocess.TimeoutExpired(cmd, kw.get("timeout"))
        return subprocess.CompletedProcess(cmd, 0, "", "")

    flow, calls = _fake_docker(tmp_path, monkeypatch, run_impl)
    m = flow.run_pnr(CFG, tmp_path, timeout_s=60)
    runs = [c for c in calls if c[:2] == ["docker", "run"]]
    kills = [c for c in calls if c[:2] == ["docker", "kill"]]
    name = runs[0][runs[0].index("--name") + 1]
    assert len(runs) == 1
    assert kills and kills[0][-1] == name
    assert m["verdict"] == "fail" and "timeout" in m["reason"]


def test_run_pnr_default_timeout_covers_a_128_neuron_run():
    # the 2026-10-17 128-neuron run took about 55 min (3300 s)
    import inspect
    from targets.digital.flow import run_pnr as rp
    assert inspect.signature(rp).parameters["timeout_s"].default >= 7200


STUB_MAKE = """#!/bin/bash
# stands in for ORFS make: writes the trees that real ORFS writes, in flow/
sub=sky130hs/snn_core_256
if [ "$2" = metadata-generate ]; then
  echo '{"finish__timing__setup__ws": 1.0}' > reports/$sub/base/metadata.json
else
  mkdir -p results/$sub/base reports/$sub/base logs/$sub/base
  echo gds > results/$sub/base/6_final.gds
  echo log > logs/$sub/base/5_2_route.log
fi
"""


def _run_script(tmp_path, script):
    import subprocess
    root, design, out, bin_ = (tmp_path / d for d in ("orfs", "design", "out", "bin"))
    for d in (root / "flow", design, out, bin_):
        d.mkdir(parents=True)
    for f in ("snn_core.v", "snn_core.sdc", "config.mk"):
        (design / f).write_text("x")
    (bin_ / "make").write_text(STUB_MAKE)
    (bin_ / "make").chmod(0o755)
    env = {"PATH": f"{bin_}:/usr/bin:/bin"}
    proc = subprocess.run(["bash", "-c", script], cwd=root, env=env,
                          capture_output=True, text=True)
    return proc, out


def test_container_script_puts_gds_metadata_and_logs_on_the_host(tmp_path):
    # executes the real script: the 2026-10-17 copy used flow/results after
    # `cd flow`, cp failed, and the script still exited 0 (#1)
    import os
    from targets.digital.flow import container_script
    script = container_script("snn_core_256", os.getuid(), os.getgid(),
                              design=str(tmp_path / "design"), out=str(tmp_path / "out"))
    proc, out = _run_script(tmp_path, script)
    assert proc.returncode == 0, proc.stderr
    assert (out / "snn_core_256/base/6_final.gds").exists()
    assert (out / "snn_core_256/base/metadata.json").exists()
    assert (out / "logs/snn_core_256/base/5_2_route.log").exists()
    assert parse_metrics(out / "snn_core_256/base")["verdict"] == "pass"


def test_container_script_fails_when_copy_out_fails(tmp_path):
    # a flow that produced nothing to copy must not report success
    import os
    from targets.digital.flow import container_script
    script = container_script("snn_core_256", os.getuid(), os.getgid(),
                              design=str(tmp_path / "design"), out=str(tmp_path / "out"))
    proc, _ = _run_script(tmp_path, script.replace("make DESIGN_CONFIG", "true DESIGN_CONFIG"))
    assert proc.returncode != 0


def test_parse_metrics_picks_final_stage_values_from_real_metadata():
    # real ORFS metadata.json (128-neuron run, 2026-10-18) holds the same
    # metric at every stage; the first-key pick returned CTS-stage values
    # (slack 33.1717, wirelength = CTS estimate 1282660) instead of the
    # finish / detailed-route values that the stage log reports (#1)
    m = parse_metrics(Path(__file__).parent / "fixtures/orfs_real_128")
    assert m["verdict"] == "pass"
    assert m["worst_slack_ns"] == 33.1432          # finish__timing__setup__ws
    assert m["pwr_w"] == 0.0141645                 # finish__power__total
    assert abs(m["area_mm2"] - 0.704933) < 1e-9    # finish__..._area__stdcell
    assert m["wirelength_um"] == 1449559           # detailedroute__route__wirelength
    assert m["drc"] == 0                           # final, not iter__0 (530)


def test_write_design_rom_raises_the_synth_memory_limit_to_the_rom_size(tmp_path):
    # yosys turns the ROM case tree into one ROM memory (128 x 510 = 65280
    # bits at 128 neurons); ORFS stops above SYNTH_MEMORY_MAX_BITS (4096 by
    # default): "Synthesized memory size 4096 exceeds SYNTH_MEMORY_MAX_BITS" (#2)
    rom = {**CFG, "neurons": 128, "weight_store": "rom"}
    write_design(rom, tmp_path / "rom")
    conf = (tmp_path / "rom/orfs/config.mk").read_text()
    assert "export SYNTH_MEMORY_MAX_BITS = 65536\n" in conf
    assert "MOCK" not in conf  # a mock memory would fake the baseline
    write_design({**CFG, "neurons": 128}, tmp_path / "ext")
    assert "SYNTH_MEMORY_MAX_BITS" not in (tmp_path / "ext/orfs/config.mk").read_text()
