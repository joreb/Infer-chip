"""OpenROAD-flow-scripts docker wrapper: write_design -> run_pnr -> GDS + metrics.

ORFS_ROOT points at a shallow clone of OpenROAD-flow-scripts (host side):
    git clone --depth 1 https://github.com/The-OpenROAD-Project/OpenROAD-flow-scripts $ORFS_ROOT
The flow runs inside the `openroad/orfs` docker image with $ORFS_ROOT and the
design staging dir bind-mounted; results land under $ORFS_ROOT/flow/results/
<platform>/<design>/<variant>/ (metadata.json is the metrics source — see
parse_metrics).
"""

import json
import re
import shutil
import subprocess
from pathlib import Path

from targets.digital.rtl_gen import generate_rtl, module_name

PLATFORM = "sky130hs"
IMAGE = "openroad/orfs:latest"

FAIL = lambda reason: {  # noqa: E731
    "verdict": "fail", "reason": reason, "area_mm2": None, "pwr_w": None,
    "worst_slack_ns": None, "drc": None, "wirelength_um": None,
}


def _pick(d: dict, pattern: str, exclude: str | None = None):
    for k, v in d.items():
        if pattern in k and (exclude is None or exclude not in k):
            return v
    return None


def parse_metrics(results_dir: Path) -> dict:
    """Extract metrics from an ORFS results dir (metadata.json preferred).

    Robust to ORFS metric-key renames: flexible substring picks, preferring
    finish-stage keys over earlier stages.
    """
    md = None
    for cand in sorted(Path(results_dir).rglob("metadata.json")):
        with open(cand) as f:
            md = json.load(f)
        break
    if md is None:
        return FAIL("no metadata.json found under results dir")

    def first(*preds):
        for pat, ex in preds:
            v = _pick(md, pat, exclude=ex)
            if v is not None:
                return v
        return None

    slack = first(("timing__setup__ws", "percent"), ("__setup__ws", None))
    pwr = first(("power__total", None))
    drc = first(("drc_errors", None), ("design__violations", None))
    area = first(("instance__area__stdcell", None), ("instance__area", None))
    wl = first(("wirelength__estimated", None), ("wirelength", "__min"))
    if slack is None:
        data = FAIL("no setup slack metric in metadata.json")
        return data
    return {
        "verdict": "pass",
        "reason": None,
        "worst_slack_ns": float(slack),
        "pwr_w": float(pwr) if pwr is not None else None,
        "drc": int(drc) if drc is not None else None,
        # ORFS areas are um^2
        "area_mm2": float(area) / 1e6 if area is not None else None,
        "wirelength_um": float(wl) if wl is not None else None,
    }


def write_design(cfg: dict, out_dir: Path) -> dict:
    """Stage design source + ORFS config.mk under out_dir/orfs/. Returns paths."""
    stage = Path(out_dir) / "orfs"
    stage.mkdir(parents=True, exist_ok=True)
    name = module_name(cfg)
    rtl = stage / "snn_core.v"
    rtl.write_text(generate_rtl(cfg))
    config = stage / "config.mk"
    config.write_text(
        f"export DESIGN_NAME = {name}\n"
        f"export DESIGN_NICKNAME = {name}\n"
        "export DESIGN_TOPLEVEL = snn_core\n"
        f"export PLATFORM = {PLATFORM}\n"
        "export VERILOG_FILES = ./designs/src/snn_core_v/snn_core.v\n"
        "export SDC_FILE = ./designs/src/snn_core_v/snn_core.sdc\n"
        f"export CORE_UTILIZATION = {cfg.get('util_target', 60)}\n"
        f"export CLOCK_PERIOD = {float(cfg.get('clock_ns', 4.0))}\n"
        "export CLOCK_PORT = clk\n"
    )
    (stage / "snn_core.sdc").write_text(
        f"create_clock -name clk -period {float(cfg.get('clock_ns', 4.0))} "
        "{[get_ports clk]}\n"
    )
    return {"config": config, "rtl": rtl, "design_name": name}


def run_pnr(cfg: dict, out_dir: Path, timeout_s: int = 3600) -> dict:
    """Synthesize + place + route in ORFS docker. Returns metrics; never raises."""
    if shutil.which("docker") is None:
        return FAIL("docker not available")
    orfs_root = Path(__import__("os").environ.get("ORFS_ROOT", "") or
                     Path.home() / "OpenROAD-flow-scripts")
    if not (orfs_root / "flow").exists():
        return FAIL(f"ORFS_ROOT missing flow dir: {orfs_root} (shallow clone "
                    "OpenROAD-flow-scripts and export ORFS_ROOT)")

    stage = write_design(cfg, Path(out_dir))
    name = stage["design_name"]
    vname = f"{name}_v"
    src = orfs_root / "flow" / "designs" / "src" / vname
    src.mkdir(parents=True, exist_ok=True)
    shutil.copy(stage["rtl"], src / "snn_core.v")
    shutil.copy(Path(out_dir) / "orfs" / "snn_core.sdc", src / "snn_core.sdc")
    cfg_dpath = orfs_root / "flow" / "designs" / PLATFORM / f"{name}.mk"
    cfg_dpath.write_text((Path(out_dir) / "orfs" / "config.mk").read_text())

    cmd = (
        f"cd /OpenROAD-flow-scripts/flow && "
        f"make DESIGN_CONFIG=./designs/{PLATFORM}/{name}.mk run -j0 2>&1 "
        "| tail -5"
    )
    docker_cmd = [
        "docker", "run", "--rm", "-u", str(__import__("os").getuid()),
        "-v", f"{orfs_root}:/OpenROAD-flow-scripts", "--workdir", "/OpenROAD-flow-scripts",
        IMAGE, "bash", "-c", cmd,
    ]
    for attempt in range(2):
        try:
            proc = subprocess.run(docker_cmd, capture_output=True, text=True,
                                  timeout=timeout_s)
            if proc.returncode == 0:
                break
            reason = f"orfs make exited {proc.returncode}: {proc.stdout[-400:]}"
        except subprocess.TimeoutExpired:
            reason = f"orfs make timeout {timeout_s}s"
        if attempt == 1:
            return FAIL(reason)
    results = orfs_root / "flow" / "results" / PLATFORM / name / "base"
    m = parse_metrics(results)
    if m["verdict"] == "fail":
        return m
    out = Path(out_dir)
    gds = results / "6_final.gds"
    if gds.exists():
        shutil.copy(gds, out / "final.gds")
    return m