"""Performance plots of the 128-neuron digital core, from git-tracked data only.

Every figure carries an honesty stamp: MEASURED (from a flow run or a parity-
checked simulation), DERIVED (arithmetic on measured values) or PROJECTION.

Inputs: tests/digital/fixtures/orfs_real_128/metadata.json (external, f6599c24),
runs_digital_e2e/digital/evidence/2026-10-18-*metadata.json, and the layout
images in wiki/raw/assets/pnr-128/. Output: wiki/raw/assets/plots/*.png.

    .venv/bin/python tools/plot_performance.py [--selftest]
"""

import argparse
import json
import sys
from pathlib import Path

import numpy as np

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from targets.digital.flow import parse_metrics  # noqa: E402
from targets.digital.model import LIFModel, sample_weight_ints  # noqa: E402

EV = REPO / "runs_digital_e2e/digital/evidence"
ASSETS = REPO / "wiki/raw/assets/pnr-128"
OUT = REPO / "wiki/raw/assets/plots"
CFG128 = {"neurons": 128, "fanout": 8, "weight_width": 4, "timesteps": 64,
          "util_target": 25, "clock_ns": 40.0}
STAMP = {"MEASURED": "#1b7f3b", "DERIVED": "#b26b00", "PROJECTION": "#b00020"}


def load(name: str) -> dict:
    path = {"ext128": REPO / "tests/digital/fixtures/orfs_real_128/metadata.json",
            "rom128": EV / "2026-10-18-rom-metadata.json",
            "ext16": EV / "2026-10-18-smoke16-metadata.json",
            "rom16": EV / "2026-10-18-rom16-metadata.json"}[name]
    md = json.loads(path.read_text())
    m = parse_metrics(path.parent) if path.name == "metadata.json" else _parse(md)
    return {"md": md, **m}


def _parse(md: dict) -> dict:
    # evidence files are not named metadata.json; reuse parse_metrics on a copy
    import tempfile
    with tempfile.TemporaryDirectory() as d:
        (Path(d) / "metadata.json").write_text(json.dumps(md))
        return parse_metrics(Path(d))


def tb_frames(cfg: dict) -> np.ndarray:
    """The parity testbench input (tests/digital/tb_parity.py::_frames)."""
    n, steps = int(cfg["neurons"]), int(cfg["timesteps"])
    train = np.zeros((steps, n), dtype=np.int8)
    train[1::2, [7 % n, 8 % n, 9 % n]] = 1
    return train


def simulate(cfg: dict, train: np.ndarray):
    model = LIFModel(cfg)
    out, v = np.zeros_like(train), np.zeros(train.shape, dtype=np.int64)
    for t in range(train.shape[0]):
        out[t] = model.step(train[t])
        v[t] = model.v
    return out, v


def stamp(ax, kind: str, note: str):
    ax.text(0.99, 0.99, f"{kind} · {note}", transform=ax.transAxes, ha="right", va="top",
            fontsize=8, color="white",
            bbox={"boxstyle": "round,pad=0.3", "fc": STAMP[kind], "ec": "none"})


def fig_layout(plt):
    from PIL import Image
    fig, axes = plt.subplots(1, 2, figsize=(12, 6.4))
    for ax, (tag, run, m) in zip(axes, [("external", "f6599c24", load("ext128")),
                                        ("rom", "15914a90", load("rom128"))]):
        ax.imshow(Image.open(ASSETS / f"{tag}-{run}-final_all.webp"))
        ax.set_axis_off()
        md = m["md"]
        ax.set_title(f"{'External SRAM weights' if tag == 'external' else 'On-die ROM weights'}"
                     f" (run {run})\nDRC {m['drc']} · cells {md['finish__design__instance__count__stdcell']:,}"
                     f" · die {md['finish__design__die__area'] / 1e6:.2f} mm²", fontsize=10)
        stamp(ax, "MEASURED", "ORFS sky130hs")
    fig.suptitle("128-neuron LIF core: routed layouts, DRC clean", fontsize=13)
    return fig


def fig_raster(plt):
    train = tb_frames(CFG128)
    out, v = simulate(CFG128, train)
    w = sample_weight_ints(CFG128)
    fig, axes = plt.subplots(3, 1, figsize=(10, 8), sharex=True,
                             gridspec_kw={"height_ratios": [1, 2, 1.4]})
    for ax, data, title, col in [(axes[0], train, "Input spikes (in_spk)", "#555"),
                                 (axes[1], out, "Output spikes of the 128 neurons", "#1b4f9c")]:
        t, n = np.nonzero(data)
        ax.scatter(t, n, s=8, marker="|", color=col)
        ax.set_ylim(-1, 128)
        ax.set_ylabel("neuron")
        ax.set_title(title, fontsize=10, loc="left")
    fired = [i for i in range(128) if out[:, i].any()]
    quiet = [i for i in range(128) if (w[i, 7] or w[i, 8] or w[i, 9]) and i not in fired]
    for i in fired[:3] + quiet[:1]:
        axes[2].step(range(len(v)), v[:, i], where="post", label=f"neuron {i}")
    axes[2].axhline(16, color="#b00020", ls="--", lw=1, label="threshold (16)")
    axes[2].set_ylabel("membrane v")
    axes[2].set_xlabel("timestep")
    axes[2].legend(fontsize=7, ncol=5, loc="upper left", bbox_to_anchor=(0, -0.25))
    axes[2].set_title("Membrane potential: neurons that fire, and one that the inputs inhibit",
                      fontsize=10, loc="left")
    stamp(axes[0], "MEASURED", "RTL = golden model, bit-exact parity, runs f6599c24 and 15914a90")
    fig.suptitle(f"Functional correctness: {int(out.sum())} output spikes over 64 timesteps, "
                 "0 mismatches between RTL and golden model", fontsize=12)
    fig.tight_layout()
    return fig, out


def fig_timing(plt):
    stages = ["floorplan", "globalplace", "placeopt", "detailedplace", "cts", "globalroute", "finish"]
    fig, ax = plt.subplots(figsize=(10, 5))
    for name, label, col in [("ext128", "external SRAM", "#1b4f9c"), ("rom128", "on-die ROM", "#c05a00")]:
        md = load(name)["md"]
        ys = [md.get(f"{s}__timing__setup__ws") for s in stages]
        ax.plot(stages, ys, "o-", color=col, label=f"{label}: final slack +{ys[-1]:.2f} ns")
    ax.axhline(0, color="#b00020", lw=1)
    ax.set_ylim(-2, 40)
    ax.axhspan(-2, 0, color="#b00020", alpha=0.08)
    ax.text(0.05, -1.4, "timing failure region (slack < 0)", color="#b00020", fontsize=8)
    ax.set_ylabel("worst setup slack (ns), clock period 40 ns")
    ax.set_title("Timing closes at every stage with more than 32 ns of margin", fontsize=12)
    ax.legend(loc="center right")
    stamp(ax, "MEASURED", "metadata.json; SDC constrains the clock only, no I/O delays")
    fig.tight_layout()
    return fig


def fig_rom_vs_ext(plt):
    metrics = [("area_mm2", "Area"), ("pwr_w", "Power"), ("wirelength_um", "Wirelength"),
               ("worst_slack_ns", "Slack")]
    fig, ax = plt.subplots(figsize=(10, 5))
    x = np.arange(len(metrics))
    for k, (n, col) in enumerate([(16, "#8fb3e0"), (128, "#1b4f9c")]):
        e, r = load(f"ext{n}"), load(f"rom{n}")
        ratios = [r[m] / e[m] for m, _ in metrics]
        bars = ax.bar(x + (k - 0.5) * 0.38, ratios, 0.36, color=col, label=f"{n} neurons")
        ax.bar_label(bars, fmt="%.3f", fontsize=8)
    ax.axhline(1.0, color="black", lw=1)
    ax.set_xticks(x, [lbl for _, lbl in metrics])
    ax.set_ylim(0, 1.45)
    ax.set_ylabel("on-die ROM / external SRAM")
    ax.set_title("Moving the weights on die: +5% area, +26% wire, timing unchanged (128 neurons)",
                 fontsize=11)
    ax.legend(loc="upper left")
    stamp(ax, "MEASURED", "external area excludes its SRAM")
    fig.tight_layout()
    return fig


def fig_throughput(plt, out: np.ndarray):
    md = load("ext128")
    pad, clk_ns = 128, 40.0
    fires = out.sum(axis=1)
    cycles = pad + 4 + fires  # IDLE latch + RUN (PAD+1) + UPDATE + EMIT; ±1 cycle
    t_us = cycles * clk_ns / 1e3
    e_nj = md["pwr_w"] * t_us * 1e3
    w = sample_weight_ints(CFG128)
    events = tb_frames(CFG128) @ (w != 0).sum(axis=0)
    fig, axes = plt.subplots(1, 3, figsize=(13, 4.3))
    axes[0].bar(range(len(t_us)), t_us, color="#1b4f9c")
    axes[0].set_ylim(0, t_us.max() * 1.3)
    axes[0].set_title(f"Time per timestep: {t_us.mean():.2f} µs\n"
                      f"= {1e6 / t_us.mean():,.0f} timesteps/s at 25 MHz", fontsize=10)
    axes[0].set_xlabel("timestep")
    axes[0].set_ylabel("µs")
    axes[1].bar(range(len(e_nj)), e_nj, color="#c05a00")
    axes[1].set_ylim(0, e_nj.max() * 1.3)
    axes[1].set_title(f"Energy per timestep: {e_nj.mean():.0f} nJ\n"
                      f"(power {md['pwr_w'] * 1e3:.2f} mW × time)", fontsize=10)
    axes[1].set_xlabel("timestep")
    axes[1].set_ylabel("nJ")
    axes[2].bar(["gated adds\n(dense, fixed)", "real synaptic\nevents (avg)", "stored\nsynapses"],
                [128 * 128, events.mean(), int((w != 0).sum())],
                color=["#999", "#1b7f3b", "#1b4f9c"])
    axes[2].set_yscale("log")
    axes[2].set_title("Work per timestep (log scale)", fontsize=10)
    for ax in axes:
        stamp(ax, "DERIVED", "ORFS power, default activity, SRAM excluded")
    fig.suptitle("Throughput and energy at the 40 ns target clock (testbench input)", fontsize=12)
    fig.tight_layout()
    return fig, t_us.mean(), e_nj.mean(), events.mean()


def fig_scaling(plt):
    ns = np.array([16, 128])
    e16, e128 = load("ext16"), load("ext128")
    area = np.array([e16["area_mm2"], e128["area_mm2"]])
    wl = np.array([e16["wirelength_um"], e128["wirelength_um"]]) / 1e6
    fig, ax = plt.subplots(figsize=(10, 5.5))
    proj = np.array([128, 256, 512, 1024])
    for y, label, col in [(area, "core cell area (mm²)", "#1b4f9c"),
                          (wl, "routed wirelength (m)", "#1b7f3b")]:
        k = np.log(y[1] / y[0]) / np.log(ns[1] / ns[0])
        ax.loglog(ns, y, "o-", color=col, label=f"{label}, measured, slope {k:.2f}")
        ax.loglog(proj, y[1] * (proj / 128) ** k, "--", color=col, alpha=0.6)
    # OpenRAM 6T on sky130hd, 148,413 bits/mm² (ORRAM paper, arXiv 2607.12244, simulated)
    sram = np.array([16, 128, 256, 512, 1024]) ** 2 * 4 / 148_413
    ax.loglog([16, 128, 256, 512, 1024], sram, "s:", color="#b00020",
              label="weight SRAM area (mm²), N² × 4 bits at OpenRAM density, PROJECTION, slope 2")
    ax.set_xlabel("neurons")
    ax.set_ylabel("mm² (area) or m (wirelength)")
    ax.set_title("Core grows about linearly with N; the dense weight memory grows as N²", fontsize=12)
    ax.legend(fontsize=8, loc="upper left")
    stamp(ax, "MEASURED", "16 and 128 neurons; dashed = PROJECTION")
    fig.tight_layout()
    return fig


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()
    e, r = load("ext128"), load("rom128")
    assert e["worst_slack_ns"] == 33.1432 and abs(e["area_mm2"] - 0.704933) < 1e-9
    assert r["wirelength_um"] == 1826253 and r["drc"] == 0
    if args.selftest:
        out, _ = simulate(CFG128, tb_frames(CFG128))
        assert out.shape == (64, 128)
        print("selftest ok")
        return 0
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    OUT.mkdir(parents=True, exist_ok=True)
    raster, out = fig_raster(plt)
    thr, t_us, e_nj, ev = fig_throughput(plt, out)
    figs = {"1-layout": fig_layout(plt), "2-correctness": raster, "3-timing": fig_timing(plt),
            "4-rom-vs-external": fig_rom_vs_ext(plt), "5-throughput-energy": thr,
            "6-scaling": fig_scaling(plt)}
    for name, fig in figs.items():
        fig.savefig(OUT / f"{name}.png", dpi=110, bbox_inches="tight")
        plt.close(fig)
    print(f"output spikes {int(out.sum())}, timestep {t_us:.3f} us, energy {e_nj:.1f} nJ, "
          f"events/timestep {ev:.2f}")
    print("\n".join(str(OUT / f"{n}.png") for n in figs))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
