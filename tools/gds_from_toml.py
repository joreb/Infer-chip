"""Generate a GDSII via the existing OpenROAD flow from a TOML config.

The TOML carries the digital-core config plus FPGA-resource bookkeeping
(number of LUTs, DSP slices, XADC, and a target clock rate). The resource
keys describe the board/prototype the GDS is sized for and are recorded in
the run metadata; the actual layout is produced by ORFS from the core RTL,
just like `targets.digital.flow.run_pnr`.

Example TOML:

    [core]
    neurons = 128
    fanout = 8
    weight_width = 4
    timesteps = 64
    seed = 11
    util_target = 60
    clock_ns = 4.0
    weight_store = "external"

    [resources]
    luts = 9900
    dsp_slices = 128
    xadc = 1
    best_clock_rate_mhz = 100.0

Usage:
    python tools/gds_from_toml.py --toml design.toml --out runs_gds
"""

import argparse
import json
import sys
import tomllib
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from targets.digital.flow import run_pnr


CORE_KEYS = {
    "neurons", "fanout", "weight_width", "timesteps", "seed",
    "util_target", "clock_ns", "weight_store",
}


def load_toml(path: Path) -> dict:
    with open(path, "rb") as f:
        data = tomllib.load(f)
    cfg = {}
    for section in ("core", "digital", "config"):
        if isinstance(data.get(section), dict):
            cfg.update(data[section])
    # top-level keys also count as config
    for k, v in data.items():
        if k not in ("core", "digital", "config", "resources") and k in CORE_KEYS:
            cfg[k] = v
    if "neurons" not in cfg:
        raise SystemExit("TOML must provide at least [core].neurons")
    resources = data.get("resources", {})
    return cfg, resources


def main() -> int:
    ap = argparse.ArgumentParser(description="TOML-driven GDSII generation")
    ap.add_argument("--toml", required=True, type=Path)
    ap.add_argument("--out", default="runs_gds", type=Path)
    ap.add_argument("--stage-only", action="store_true",
                    help="stage RTL + config.mk (orfs/) without invoking Docker")
    args = ap.parse_args()

    cfg, resources = load_toml(args.toml)
    out_dir = args.out.resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    run_dir = out_dir / "run"
    run_dir.mkdir(parents=True, exist_ok=True)

    if args.stage_only:
        from targets.digital.flow import write_design
        wd = write_design(cfg, run_dir)
        (out_dir / "gds_metadata.json").write_text(
            json.dumps({"config": cfg, "resources": resources,
                        "staged": str(wd["config"].parent.relative_to(out_dir)),
                        "gds": None},
                       indent=2, default=str))
        print(json.dumps({"status": "staged", "orfs_dir": str(wd["config"].parent),
                          "design_name": wd["design_name"]}, indent=2))
        return 0

    metrics = run_pnr(cfg, run_dir)
    gds = run_dir / "final.gds"
    metadata = {
        "config": cfg,
        "resources": resources,
        "metrics": metrics,
        "gds": str(gds.relative_to(out_dir)) if gds.exists() else None,
        "results_dir": str((run_dir / "results").relative_to(out_dir)),
        "fpga_name": cfg.get("fpga_name", "fpga_core"),
        "port_names": ["clk", "rst_n", "timestep_start", "in_spk", "spike_out_valid",
                       "spike_out_addr", "spike_out_data"],
    }
    (out_dir / "gds_metadata.json").write_text(json.dumps(metadata, indent=2, default=str))
    print(json.dumps(metadata, indent=2, default=str))
    return 0 if metrics.get("verdict") == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
