"""OpenROAD-flow-scripts docker wrapper: write_design -> run_pnr -> GDS + metrics.

The `openroad/orfs` image carries its own prebuilt flow tree; no host clone and
no ORFS_ROOT. Design staging (write_design output under <out_dir>/orfs/) is
bind-mounted read-in at /mnt/design and copied into the image's flow dir inside
the container; flow results are bind-mounted back out to <out_dir>/results/
<design>/<variant>/ (metadata.json is the metrics source — see parse_metrics).
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


def _num(v) -> float | None:
    """Coerce a metric value; non-numeric (e.g. "N/A") -> None, never raises."""
    try:
        f = float(v)
    except (TypeError, ValueError):
        return None
    return None if f != f else f  # NaN filter


def _pick_num(d: dict, pattern: str, exclude: str | None = None):
    """First NUMERIC value under a metric-key pattern (skips "N/A" strings,
    keys like __percent/__period, and any non-numeric metric)."""
    for k, v in d.items():
        if pattern in k and (exclude is None or exclude not in k) and _num(v) is not None:
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
            v = _pick_num(md, pat, exclude=ex)
            if v is not None:
                return v
        return None

    slack = first(("timing__setup__ws", "percent"), ("__setup__ws", "percent"))
    pwr = first(("power__total", None))
    drc = first(("drc_errors", None), ("design__violations", None))
    area = first(("instance__area__stdcell", None), ("instance__area", None))
    wl = first(("wirelength__estimated", None), ("wirelength", "__min"))
    slack_n = _num(slack)
    if slack_n is None:
        return FAIL("no setup slack metric in metadata.json")
    return {
        "verdict": "pass",
        "reason": None,
        "worst_slack_ns": slack_n,
        "pwr_w": _num(pwr),
        "drc": int(drc) if drc is not None else None,
        # ORFS areas are um^2
        "area_mm2": _num(area) / 1e6 if _num(area) is not None else None,
        "wirelength_um": _num(wl),
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
        # must equal the generated top module exactly; yosys rejects anything
        # else ("ERROR: Module `snn_core' not found!")
        f"export DESIGN_NAME = {name}\n"
        f"export DESIGN_NICKNAME = {name}\n"  # names the results dir
        f"export PLATFORM = {PLATFORM}\n"
        "export VERILOG_FILES = ./designs/src/snn_core/snn_core.v\n"
        "export SDC_FILE = ./designs/src/snn_core/snn_core.sdc\n"
        f"export CORE_UTILIZATION = {cfg.get('util_target', 60)}\n"
        f"export CLOCK_PERIOD = {float(cfg.get('clock_ns', 4.0))}\n"
        "export CLOCK_PORT = clk\n"
    )
    (stage / "snn_core.sdc").write_text(
        f"create_clock -name clk -period {float(cfg.get('clock_ns', 4.0))} "
        "[get_ports clk]\n"
    )
    return {"config": config, "rtl": rtl, "design_name": name}


def container_script(name: str, uid: int, gid: int,
                     design: str = "/mnt/design", out: str = "/results") -> str:
    """Bash script run inside the ORFS image (cwd = the ORFS checkout).

    Bare `make` never runs genMetrics: metadata.json comes only from
    `make metadata-generate`, which writes it under flow/reports/ (#1). The
    script copies results, reports and logs out, and puts metadata.json next
    to the results so parse_metrics(<results>/base) finds it.

    The `cd flow` persists for the rest of the script, so every copy path is
    relative to flow/. Before #1 the copy used flow/results/..., which then
    resolved to flow/flow/results: cp failed, and the script still exited 0.
    Now a failed copy makes the script fail.
    """
    mk = f"DESIGN_CONFIG=./designs/{PLATFORM}/{name}.mk"
    sub = f"{PLATFORM}/{name}"
    keep = "|| { [ $rc -eq 0 ] && rc=1; }"
    return (
        "set -o pipefail; "
        f"mkdir -p flow/designs/src/snn_core flow/designs/{PLATFORM} && "
        f"cp {design}/snn_core.v {design}/snn_core.sdc flow/designs/src/snn_core/ && "
        f"cp {design}/config.mk flow/designs/{PLATFORM}/{name}.mk && "
        f"cd flow && make {mk} 2>&1 | tail -5; "
        "rc=$?; "
        f"if [ $rc -eq 0 ]; then make {mk} metadata-generate 2>&1 | tail -5; rc=$?; fi; "
        f"mkdir -p {out}/{name} {out}/reports {out}/logs; "
        f"cp -r results/{sub}/. {out}/{name}/ {keep}; "
        f"cp -r reports/{sub} {out}/reports/{name} {keep}; "
        f"cp -r logs/{sub} {out}/logs/{name} {keep}; "
        f"cp reports/{sub}/base/metadata.json {out}/{name}/base/ {keep}; "
        f"chown -R {uid}:{gid} {out}; exit $rc"
    )


def run_pnr(cfg: dict, out_dir: Path, timeout_s: int = 7200) -> dict:
    """Synthesize + place + route in ORFS docker. Returns metrics; never raises.

    The openroad/orfs image carries its own prebuilt flow tree, so nothing on
    the host is mounted over it (mounting a host clone would shadow the image's
    tools/install). The staged design is copied INTO the image's flow tree
    inside the container; flow results are bind-mounted back out. Runs as root
    (writes over the image tree) and chowns the results back to the host user.
    """
    if shutil.which("docker") is None:
        return FAIL("docker not available")

    stage = write_design(cfg, Path(out_dir))
    name = stage["design_name"]
    uid = __import__("os").getuid()
    gid = __import__("os").getgid()
    results_host = Path(out_dir) / "results"
    out_results = results_host / name
    # purge stale results (ENG-003): a previous run with the same
    # DESIGN_NICKNAME would otherwise be parsed as this run's metrics
    if out_results.exists():
        shutil.rmtree(out_results)

    cmd = container_script(name, uid, gid)
    # -v bind sources must be absolute host paths: docker treats a relative
    # path as a named volume and rejects it ("invalid characters for a local
    # volume name ... use absolute path")
    results_host.mkdir(parents=True, exist_ok=True)
    container = f"orfs-{name}-{__import__('secrets').token_hex(4)}"
    docker_cmd = [
        "docker", "run", "--rm", "--name", container,
        "-u", "0:0",  # writes over the root-owned image tree
        "-v", f"{stage_dir(out_dir).resolve()}:/mnt/design",
        "-v", f"{results_host.resolve()}:/results",
        IMAGE, "bash", "-c", cmd,
    ]
    # record the exact command: the 2026-10-17 artifact loss could not be
    # traced because the wrapper's mounts were never written down (#1)
    (Path(out_dir) / "docker_cmd.txt").write_text(
        " ".join(__import__("shlex").quote(a) for a in docker_cmd) + "\n")
    for attempt in range(2):
        try:
            proc = subprocess.run(docker_cmd, capture_output=True, text=True,
                                  timeout=timeout_s)
            if proc.returncode == 0:
                break
            reason = (f"orfs make exited {proc.returncode}: "
                      f"{proc.stdout[-400:]}{proc.stderr[-400:]}")
        except subprocess.TimeoutExpired:
            # the timeout kills the docker CLI, not the container; a retry
            # would start a second ORFS run beside the first one
            subprocess.run(["docker", "kill", container], capture_output=True)
            return FAIL(f"orfs make timeout {timeout_s}s")
        if attempt == 1:
            return FAIL(reason)
    m = parse_metrics(out_results / "base")
    if m["verdict"] == "fail":
        return m
    gds = out_results / "base" / "6_final.gds"
    if gds.exists():
        shutil.copy(gds, Path(out_dir) / "final.gds")
    return m


def stage_dir(out_dir: Path) -> Path:
    """Host-side design staging dir that the container reads as /mnt/design."""
    out_dir.mkdir(parents=True, exist_ok=True)
    return Path(out_dir) / "orfs"