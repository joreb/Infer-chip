import json
import runpy
import subprocess
import sys
from pathlib import Path

import pytest


SCRIPT = Path(__file__).resolve().parents[1] / "tools" / "complex128_to_gds.py"
REPO = SCRIPT.parents[1]


def test_help_does_not_start_flow(monkeypatch, capsys):
    calls = []

    def record_call(*args, **kwargs):
        calls.append((args, kwargs))
        raise AssertionError("Docker must not start for --help")

    monkeypatch.setattr(subprocess, "run", record_call)
    monkeypatch.setattr(sys, "argv", [str(SCRIPT), "--help"])

    try:
        runpy.run_path(str(SCRIPT), run_name="__main__")
    except SystemExit as exc:
        assert exc.code == 0
    else:
        raise AssertionError("argparse did not handle --help")

    assert calls == []
    help_text = capsys.readouterr().out
    assert "--src" in help_text
    assert "--out" in help_text
    assert "--name" in help_text


def test_parallel_sources_stage_and_gds_copy(monkeypatch, tmp_path):
    from tools import complex128_to_gds

    real_run = subprocess.run
    out = tmp_path / "gds"
    name = "complex128_gpu_128"

    def fake_orfs(cmd, **kwargs):
        base = out / "run" / "results" / name / "base"
        base.mkdir(parents=True)
        (base / "metadata.json").write_text(json.dumps({
            "finish__timing__setup__ws": 1.25,
            "finish__power__total": 0.1,
            "detailedroute__route__drc_errors": 0,
            "finish__design__instance__area__stdcell": 1000000,
            "detailedroute__route__wirelength": 100,
        }))
        (base / "6_final.gds").write_bytes(b"fresh parallel gds")
        return subprocess.CompletedProcess(cmd, 0, stdout="", stderr="")

    monkeypatch.setattr(complex128_to_gds.subprocess, "run", fake_orfs)
    monkeypatch.setattr(sys, "argv", [
        str(SCRIPT),
        "--src", "spikes/complex128-unit/complex128_gpu_128.v",
        "--out", str(out),
        "--name", name,
    ])

    assert complex128_to_gds.main() == 0
    assert (out / "run" / "final.gds").read_bytes() == b"fresh parallel gds"
    config = (out / "run" / "orfs" / "config.mk").read_text()
    assert f"export DESIGN_NAME = {name}\n" in config
    assert "export SYNTH_HIERARCHICAL = 1\n" in config
    assert "export SYNTH_KEEP_MODULES = complex128_unit\n" in config

    simulation = tmp_path / "staged_tb"
    real_run([
        "iverilog", "-g2012", "-o", str(simulation),
        str(out / "run" / "orfs" / "snn_core.v"),
        str(REPO / "spikes/complex128-unit/complex128_gpu_128_tb.sv"),
    ], check=True, cwd=REPO)
    result = real_run([str(simulation)], check=True, capture_output=True, text=True)
    assert "PASS: 128 parallel complex lanes" in result.stdout


def test_timeout_kills_same_container(monkeypatch, tmp_path, capsys):
    from tools import complex128_to_gds

    killed = []
    name = "complex128_gpu_128"

    def fake_run(cmd, **kwargs):
        if cmd[1] == "run":
            raise subprocess.TimeoutExpired(cmd, 7200, output="synthesis timeout")
        if cmd[1] == "kill":
            killed.append(cmd[2])
            return subprocess.CompletedProcess(cmd, 0, stdout="", stderr="")
        raise AssertionError(f"unexpected command: {cmd}")

    monkeypatch.setattr(complex128_to_gds.subprocess, "run", fake_run)
    monkeypatch.setattr(sys, "argv", [
        str(SCRIPT), "--src", "spikes/complex128-unit/complex128_gpu_128.v",
        "--out", str(tmp_path / "gds"), "--name", name,
    ])

    assert complex128_to_gds.main() != 0
    assert len(killed) == 1
    assert killed[0].startswith(f"orfs-{name}-")
    assert "synthesis timeout" in capsys.readouterr().out


@pytest.mark.parametrize("failure", ["docker", "missing_gds", "bad_metrics"])
def test_failed_run_removes_stale_gds(monkeypatch, tmp_path, failure):
    from tools import complex128_to_gds

    out = tmp_path / "gds"
    name = "complex128_gpu_128"
    final_gds = out / "run" / "final.gds"
    final_gds.parent.mkdir(parents=True)
    final_gds.write_bytes(b"stale gds")

    def fake_orfs(cmd, **kwargs):
        if failure == "docker":
            return subprocess.CompletedProcess(cmd, 2, stdout="ORFS failed", stderr="")
        base = out / "run" / "results" / name / "base"
        base.mkdir(parents=True)
        metadata = {} if failure == "bad_metrics" else {
            "finish__timing__setup__ws": 1.25,
        }
        (base / "metadata.json").write_text(json.dumps(metadata))
        return subprocess.CompletedProcess(cmd, 0, stdout="", stderr="")

    monkeypatch.setattr(complex128_to_gds.subprocess, "run", fake_orfs)
    monkeypatch.setattr(sys, "argv", [
        str(SCRIPT), "--src", "spikes/complex128-unit/complex128_gpu_128.v",
        "--out", str(out), "--name", name,
    ])

    assert complex128_to_gds.main() != 0
    assert not final_gds.exists()
