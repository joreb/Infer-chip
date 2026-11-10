"""Veryl -> RTL -> GDSII via OpenROAD."""
import shutil, subprocess, sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SRC = REPO / "spikes" / "veryl-lif" / "target" / "main.sv"
OUT = REPO / "runs_veryl_gds"
stage = OUT / "run" / "orfs"
if stage.exists():
    shutil.rmtree(stage)
stage.mkdir(parents=True, exist_ok=True)
combined = SRC.read_text()
(stage / "snn_core.v").write_text(combined)
(stage / "snn_core.sdc").write_text("create_clock -name clk -period 10.0 [get_ports clk]\n")

name = "veryl_lif_LifStep"
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

if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))
from targets.digital.flow import container_script, parse_metrics

uid = __import__("os").getuid()
gid = __import__("os").getgid()
results_host = OUT / "run" / "results"
if results_host.exists():
    shutil.rmtree(results_host)
results_host.mkdir(parents=True, exist_ok=True)

cmd = container_script(name, uid, gid)
container = f"orfs-{name}-{__import__('secrets').token_hex(4)}"
docker_cmd = ["docker","run","--rm","--name",container,"-u","0:0",
    "-v", f"{stage.resolve()}:/mnt/design",
    "-v", f"{results_host.resolve()}:/results",
    "openroad/orfs:latest","bash","-c",cmd]
proc = subprocess.run(docker_cmd, capture_output=True, text=True, timeout=7200)
print("docker rc:", proc.returncode)
if proc.returncode != 0:
    print(proc.stdout[-500:]); print(proc.stderr[-500:])

m = parse_metrics((results_host / name)/ "base")
print("metrics:", m)
gds = (results_host / name)/ "base" / "6_final.gds"
if gds.exists():
    shutil.copy(gds, OUT / "run" / "final.gds")
    print("GDS:", OUT / "run" / "final.gds")
