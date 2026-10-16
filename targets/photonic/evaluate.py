"""PhotonicTarget.evaluate: seeded benchmark workload through MeshModel.

Sim and flow are both model-level here: sim = accuracy check (max_err below
bound), flow = deterministic PPA (energy/loss/footprint). A fixed seeded
workload pins round-to-round comparability for the journal.
"""

import numpy as np
from pathlib import Path

from targets.base import Target
from targets.photonic.mesh import MeshModel

MAX_ERR_BOUND = 0.05
N_MODES = 16
BATCH = 8
DEPTH_BENCH = 8


DEFAULT_CFG = {"mesh_depth": 4, "precision_bits": 8, "laser_mw": 1.0,
               "wavelength_nm": 1550}


class PhotonicTarget(Target):
    name = "photonic"
    required_keys = ["mesh_depth", "precision_bits", "laser_mw", "wavelength_nm"]
    DEFAULT_CFG = DEFAULT_CFG

    def _workload(self) -> tuple[np.ndarray, np.ndarray]:
        rng = np.random.default_rng(42)
        inputs = rng.random((BATCH, N_MODES))
        weights = rng.uniform(-1.0, 1.0, (N_MODES, N_MODES))
        return inputs, weights

    def evaluate(self, cfg: dict, out_dir: Path) -> dict:
        inputs, weights = self._workload()
        out, metrics = MeshModel(cfg).run(inputs, weights)
        sim = dict(metrics)
        sim["verdict"] = "pass" if metrics["max_err"] < MAX_ERR_BOUND else "fail"
        if sim["verdict"] == "fail":
            sim["reason"] = f"max_err {metrics['max_err']:.4g} >= {MAX_ERR_BOUND}"
        # flow = deterministic PPA derived from the same model (config-only)
        flow = {"verdict": "pass", "loss_db": metrics["loss_db"],
                "footprint_mm2": metrics["footprint_mm2"],
                "energy_per_mac_pj": metrics["energy_per_mac_pj"]}
        return {"sim": sim, "flow": flow, "config": cfg}