"""Photonic SVD-mesh core against the digital LIF core: same task, same plots style.

Task: the per-timestep synaptic product I = W @ s of the 128-neuron SNN,
followed by the same integer LIF update. Digital values are measured (ORFS)
or derived from measured values; photonic values are layout geometry
(gdsfactory generic PDK, no foundry DRC) plus the model in
targets/photonic/svd_mesh.py. Constants marked ASSUMED are swept as ranges.

    .venv/bin/python tools/plot_photonic_vs_digital.py [--selftest]
"""

import argparse
import json
import sys
from pathlib import Path

import numpy as np

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from targets.digital.model import LIFModel  # noqa: E402
from targets.photonic.svd_mesh import photonic_lif_run  # noqa: E402

PH = REPO / "wiki/raw/assets/photonic"
DIG = REPO / "wiki/raw/assets/pnr-128"
EV = REPO / "runs_digital_e2e/digital/evidence"
OUT = REPO / "wiki/raw/assets/plots"
CFG = {"neurons": 128, "fanout": 8, "weight_width": 4, "timesteps": 64,
       "util_target": 25, "clock_ns": 40.0}
STAMP = {"MEASURED": "#1b7f3b", "DERIVED": "#b26b00", "PROJECTION": "#b00020",
         "ASSUMED": "#5b2a86", "MODEL": "#30577a"}

# ASSUMED ranges (not from a measured device in this project)
HEATER_MW = (1.0, 20.0)        # thermo-optic phase-shifter hold power per heater
LASER_ELEC_MW = (5e3, 5e4)     # 1 to 10 W optical (accuracy sweep, 0.02 dB/MZI) at 20% wall-plug
E_MOD_PJ = (0.01, 1.0)         # per input modulation per timestep
E_ADC_PJ = (1.0, 10.0)         # per output conversion (receiver + ADC)
MAX_RATE_HZ = 1e9              # modulator and ADC sample rate, upper bound
NG = 4.2                       # silicon waveguide group index
# digital, DERIVED from measured run f6599c24 (see 128-neuron performance page)
DIG_T_US, DIG_E_NJ, DIG_AREA128 = 5.29, 74.9, None


def stamp(ax, kind, note, loc=(0.99, 0.99)):
    ax.text(*loc, f"{kind} · {note}", transform=ax.transAxes, ha="right", va="top", fontsize=7.5,
            color="white", bbox={"boxstyle": "round,pad=0.3", "fc": STAMP[kind], "ec": "none"})


def areas():
    ph = json.loads((PH / "layout_areas.json").read_text())
    d16 = json.loads((EV / "2026-10-18-smoke16-metadata.json").read_text())
    d128 = json.loads((REPO / "tests/digital/fixtures/orfs_real_128/metadata.json").read_text())
    return ph, {16: d16["finish__design__die__area"] / 1e6, 128: d128["finish__design__die__area"] / 1e6}


def project(ph, n):
    ns = np.array([r["n"] for r in ph], float)
    w = np.polyfit(ns, [r["width_um"] for r in ph], 1)
    h = np.polyfit(ns, [r["height_um"] for r in ph], 1)
    return np.polyval(w, n), np.polyval(h, n)


def fig_layout(plt):
    from PIL import Image
    ph, dig = areas()
    p16 = next(r for r in ph if r["n"] == 16)
    side = np.sqrt(dig[16]) * 1e3  # um
    fig, ax = plt.subplots(figsize=(13, 3.2))
    ax.imshow(Image.open(PH / "svd_mesh_16_full.png"), extent=[0, p16["width_um"], 700, 700 + p16["height_um"]],
              aspect="auto")
    ax.imshow(Image.open(DIG / "external-c1211375-16-final_all.webp"), extent=[0, side, 0, side])
    ax.set_xlim(-100, p16["width_um"] + 100)
    ax.set_ylim(-50, 700 + p16["height_um"] + 160)
    ax.set_aspect("equal")
    ax.set_xlabel("µm (same scale for both)")
    ax.set_yticks([])
    ax.text(p16["width_um"] / 2, 700 + p16["height_um"] + 30,
            f"Photonic SVD mesh, N = 16: {p16['width_um'] / 1e3:.1f} × {p16['height_um'] / 1e3:.2f} mm "
            f"= {p16['bbox_mm2']:.2f} mm², {p16['mzi']} MZIs + {p16['attenuator']} attenuators "
            f"(optics only)", ha="center", fontsize=9)
    ax.text(side + 120, side / 2, f"Digital LIF core, 16 neurons: die {dig[16]:.3f} mm², DRC 0 "
            "(run c1211375, includes all logic)", va="center", fontsize=9)
    stamp(ax, "MEASURED", "digital: ORFS sky130hs; photonic: gdsfactory generic PDK geometry, no foundry DRC",
          loc=(0.99, 0.30))
    fig.tight_layout()
    return fig


def fig_area(plt):
    ph, dig = areas()
    ns = np.array([4, 8, 16, 32, 64, 128])
    fig, ax = plt.subplots(figsize=(9.5, 5.2))
    meas = [r for r in ph]
    ax.loglog([r["n"] for r in meas], [r["bbox_mm2"] for r in meas], "o-", color="#30577a",
              label="photonic mesh bounding box, measured (gdsfactory)")
    w, h = project(ph, ns)
    ax.loglog(ns, w * h / 1e6, "--", color="#30577a", alpha=0.6, label="photonic, PROJECTION (linear W and H fit)")
    ax.loglog(list(dig), list(dig.values()), "s-", color="#1b4f9c", label="digital die area, measured (ORFS)")
    ax.axhline(858, color="#b00020", ls=":", lw=1)
    ax.text(4.2, 960, "one reticle field, 26 × 33 mm = 858 mm²", color="#b00020", fontsize=8)
    w128, h128 = project(ph, 128)
    ax.annotate(f"N = 128: {w128 / 1e3:.0f} mm × {h128 / 1e3:.1f} mm\n= {w128 * h128 / 1e6:.0f} mm², "
                "longer than a reticle", (128, w128 * h128 / 1e6), (20, 200), fontsize=8,
                arrowprops={"arrowstyle": "->"})
    ax.set_xlabel("neurons (matrix size N)")
    ax.set_ylabel("area (mm²)")
    ax.set_title("Area: the photonic mesh grows as N² MZIs; the digital core grows about as N", fontsize=11)
    ax.legend(fontsize=8, loc="lower right")
    stamp(ax, "MEASURED", "N ≤ 16 photonic, 16 and 128 digital; dashed = PROJECTION; photonic excludes electronics")
    fig.tight_layout()
    return fig


def fig_accuracy(plt):
    rng = np.random.default_rng(0)
    train = (rng.random((CFG["timesteps"], CFG["neurons"])) < 0.2).astype(np.int8)
    golden = LIFModel(CFG).run(train)

    def err(**kw):
        return np.mean([np.mean(photonic_lif_run(CFG, train, seed=s, **kw) != golden) for s in range(3)])

    base = {"phase_bits": None, "phase_noise_rad": 0.0, "laser_mw": None, "adc_bits": None}
    sweeps = [("phase_bits", [4, 6, 8, 10, 12, 14], "phase resolution (bits)", False),
              ("phase_noise_rad", [1e-4, 3e-4, 1e-3, 3e-3, 1e-2, 3e-2], "phase noise σ (rad)", True),
              ("laser_mw", [1, 10, 100, 1e3, 1e4, 1e5], "laser optical power (mW)", True),
              ("adc_bits", [6, 8, 10, 12, 14], "ADC resolution (bits)", False)]
    fig, axes = plt.subplots(1, 4, figsize=(15, 4))
    for ax, (key, vals, label, logx) in zip(axes, sweeps):
        if key == "laser_mw":
            for loss, col in [(0.02, "#30577a"), (0.1, "#8aa2bd")]:
                ys = [err(**{**base, key: v}, loss_db_per_mzi=loss) * 100 for v in vals]
                ax.plot(vals, ys, "o-", color=col, label=f"{loss} dB/MZI loss (ASSUMED)")
            ax.legend(fontsize=7, loc="center right")
        else:
            ys = [err(**{**base, key: v}) * 100 for v in vals]
            ax.plot(vals, ys, "o-", color="#30577a", label="photonic")
        ax.axhline(0, color="#1b4f9c", lw=2, label="digital: 0 (bit-exact)")
        if logx:
            ax.set_xscale("log")
        ax.set_xlabel(label, fontsize=9)
        ax.set_ylim(-1, max(5, max(ys) * 1.15))
        stamp(ax, "MODEL", "1 knob at a time, others ideal" + (", 1 nW noise ASSUMED" if key == "laser_mw" else ""))
    axes[0].set_ylabel("wrong spikes (% of neuron-timesteps)")
    axes[0].legend(fontsize=8)
    fig.suptitle("Accuracy: the photonic product must be good to about one weight step, or spikes change "
                 "(128 neurons, random input p = 0.2)", fontsize=11)
    fig.tight_layout()
    return fig


def photonic_energy(rate_hz, n=128, lo=True):
    pick = 0 if lo else 1
    heaters = n * (n - 1) + 2 * n  # two meshes + attenuators + sign column
    static_w = heaters * HEATER_MW[pick] / 1e3 + LASER_ELEC_MW[pick] / 1e3
    dyn_j = n * (E_MOD_PJ[pick] + E_ADC_PJ[pick]) * 1e-12
    return (static_w / rate_hz + dyn_j) * 1e9  # nJ per timestep


def fig_energy(plt):
    ph, _ = areas()
    w128, _ = project(ph, 128)
    t_prop_ns = w128 * 1e-6 * NG / 3e8 * 1e9
    rates = np.logspace(4, 9, 60)
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    ax = axes[0]
    ax.fill_between(rates, photonic_energy(rates, lo=True), photonic_energy(rates, lo=False),
                    color="#30577a", alpha=0.3, label="photonic, ASSUMED range")
    ax.loglog(rates, photonic_energy(rates, lo=True), color="#30577a", lw=1)
    ax.loglog(rates, photonic_energy(rates, lo=False), color="#30577a", lw=1)
    ax.loglog([1e6 / DIG_T_US], [DIG_E_NJ], "s", color="#1b4f9c", ms=9,
              label=f"digital: {DIG_E_NJ:.0f} nJ at {1e6 / DIG_T_US / 1e3:.0f}k timesteps/s (DERIVED)")
    ax.axvline(1e6 / DIG_T_US, color="#1b4f9c", ls=":", lw=1)
    ax.set_xlabel("timesteps per second")
    ax.set_ylabel("energy per timestep (nJ)")
    ax.set_title("Energy: static heater and laser power dominate unless the photonic core runs near 1 GHz",
                 fontsize=10)
    ax.legend(fontsize=8, loc="upper right", bbox_to_anchor=(1, 0.9))
    stamp(ax, "ASSUMED", f"heaters {HEATER_MW[0]:g} to {HEATER_MW[1]:g} mW × 16,512; laser 5 to 50 W electrical; ADC, modulator")
    ax = axes[1]
    bars = ax.bar(["digital\n(measured design,\n40 ns clock)", "photonic\nlight propagation\n(N = 128 path)",
                   "photonic\nat 1 GS/s I/O\n(ASSUMED limit)"],
                  [DIG_T_US * 1e3, t_prop_ns, 1e9 / MAX_RATE_HZ + t_prop_ns],
                  color=["#1b4f9c", "#30577a", "#5b6f8a"])
    ax.bar_label(bars, fmt="%.1f ns", fontsize=9)
    ax.set_yscale("log")
    ax.set_ylabel("latency per timestep (ns)")
    ax.set_title("Latency: light crosses the 128-mode mesh in about 1.3 ns", fontsize=10)
    stamp(ax, "DERIVED", f"path {w128 / 1e3:.0f} mm × group index {NG} / c")
    fig.tight_layout()
    return fig, t_prop_ns


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()
    ph, dig = areas()
    assert abs(dig[16] - 0.277518) < 1e-9 and {r["n"] for r in ph} >= {4, 8, 16}
    # at the digital timestep rate, the photonic heaters alone cost more than the digital core
    assert photonic_energy(1e6 / DIG_T_US, lo=True) > 100 * DIG_E_NJ
    if args.selftest:
        print("selftest ok")
        return 0
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    figs = {"7-photonic-layout-vs-digital": fig_layout(plt), "8-photonic-area": fig_area(plt),
            "9-photonic-accuracy": fig_accuracy(plt)}
    figs["10-photonic-energy-latency"], t_ns = fig_energy(plt)
    for name, fig in figs.items():
        fig.savefig(OUT / f"{name}.png", dpi=110, bbox_inches="tight")
        plt.close(fig)
    w, h = project(ph, 128)
    print(f"N=128 projection {w / 1e3:.1f} x {h / 1e3:.2f} mm = {w * h / 1e6:.0f} mm2; "
          f"propagation {t_ns:.2f} ns; photonic energy at digital rate "
          f"{photonic_energy(1e6 / DIG_T_US):.3g} to {photonic_energy(1e6 / DIG_T_US, lo=False):.3g} nJ; "
          f"at 1 GHz {photonic_energy(1e9):.3g} to {photonic_energy(1e9, lo=False):.3g} nJ")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
