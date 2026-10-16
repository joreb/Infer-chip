"""MemristiveTarget.evaluate: seeded benchmark through CrossbarModel.

Sim = accuracy check vs variability bound; flow = deterministic PPA.
"""

import numpy as np
from pathlib import Path

from targets.base import Target
from targets.memristive.crossbar import CrossbarModel

MAX_ERR_BOUND = 0.10
ROWS = COLS = 64
BATCH = 8


class MemristiveTarget(Target):
    name = "memristive"
    required_keys = ["xbar_rows", "xbar_cols", "variability_frac", "adc_bits"]

    def _workload(self) -> tuple[np.ndarray, np.ndarray]:
        rng = np.random.default_rng(42)
        inputs = (rng.random((BATCH, ROWS)) > 0.7).astype(np.float64)
        weights = rng.uniform(-7, 7, (ROWS, COLS))
        return inputs, weights

    def evaluate(self, cfg: dict, out_dir: Path) -> dict:
        inputs, weights = self._workload()
        out, metrics = CrossbarModel(cfg).run(inputs, weights)
        ideal_scale = float(np.max(np.abs(inputs @ weights))) or 1.0
        rel_err = metrics["max_err"] / ideal_scale
        sim = dict(metrics)
        sim["rel_err"] = rel_err
        sim["verdict"] = "pass" if rel_err < MAX_ERR_BOUND else "fail"
        if sim["verdict"] == "fail":
            sim["reason"] = f"rel_err {rel_err:.4g} >= {MAX_ERR_BOUND}"
        flow = {"verdict": "pass", "energy_per_mac_pj": metrics["energy_per_mac_pj"],
                "area_mm2": metrics["area_mm2"], "max_err": metrics["max_err"]}
        return {"sim": sim, "flow": flow, "config": cfg}