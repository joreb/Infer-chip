"""Spade -> RTL -> GDSII via the existing OpenROAD flow (sky130hs).

Combines the Spade-generated Verilog (spikes/spade-lif/build/spade.sv) with a
plain-Verilog wrapper, stages them as an ORFS design, runs PnR, and copies
out final.gds.
"""

import shutil
import subprocess
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SPIKE = REPO / "spikes" / "spade-lif"
OUT = REPO / "runs_spade_gds"

# Combine Spade RTL + wrapper into one design file (ORFS reads one file path).
spade_sv = (SPIKE / "build" / "spade.sv").read_text()
wrapper = (SPIKE / "wrapper.v").read_text()
combined = spade_sv + "\n" + wrapper + "\n"

stage = OUT / "run" / "orfs"
if stage.exists():
    shutil.rmtree(stage)
stage.mkdir(parents=True, exist_ok=True)
(stage / "snn_core.v").write_text(combined)
(stage / "snn_core.sdc").write_text("create_clock -name clk -period 10.0 [get_ports clk]\n")

name = "spade_lif_wrapper"
cfg_text = (
    f"export DESIGN_NAME = {name}\n"
    f"export DESIGN_NICKNAME = {name}\n"
    "export PLATFORM = sky130hs\n"
    "export VERILOG_FILES = ./designs/src/snn_core/snn_core.v\n"
    "export SDC_FILE = ./designs/src/snn_core/snn_core.sdc\n"
    "export CORE_UTILIZATION = 40\n"
    "export CLOCK_PERIOD = 10.0\n"
    "export CLOCK_PORT = clk\n"
)
(stage / "config.mk").write_text(cfg_text)

sys_path = str(REPO)
import sys as _sys
if sys_path not in _sys.path:
    _sys.path.insert(0, sys_path)
from targets.digital.flow import container_script, parse_metrics

uid = __import__("os").getuid()
gid = __import__("os").getgid()
results_host = OUT / "run" / "results"
if results_host.exists():
    shutil.rmtree(results_host)
results_host.mkdir(parents=True, exist_ok=True)

cmd = container_script(name, uid, gid)
container = f"orfs-{name}-{__import__('secrets').token_hex(4)}"
docker_cmd = [
    "docker", "run", "--rm", "--name", container,
    "-u", "0:0",
    "-v", f"{stage.resolve()}:/mnt/design",
    "-v", f"{results_host.resolve()}:/results",
    "openroad/orfs:latest", "bash", "-c", cmd,
]
print("Running PnR for Spade-derived wrapper...")
proc = subprocess.run(docker_cmd, capture_output=True, text=True, timeout=7200)
print("docker rc:", proc.returncode)
if proc.returncode != 0:
    print(proc.stdout[-1000:])
    print(proc.stderr[-1000:])

out_results = results_host / name
m = parse_metrics(out_results / "base")
print("metrics:", m)
gds = out_results / "base" / "6_final.gds"
if gds.exists():
    shutil.copy(gds, OUT / "run" / "final.gds")
    print("GDS:", OUT / "run" / "final.gds")
