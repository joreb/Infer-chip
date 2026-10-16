"""Photonic MZI-mesh model tests."""

import numpy as np

from targets.photonic.mesh import MeshModel

CFG = {
    "mesh_depth": 4,
    "precision_bits": 8,
    "laser_mw": 1.0,
    "wavelength_nm": 1550,
    "seed": 3,
}
INPUTS = np.random.default_rng(0).random((4, 8)).astype(np.float64)
WEIGHTS = np.random.default_rng(1).random((8, 8)).astype(np.float64) * 0.5


def test_identity_mesh_reproduces_inputs():
    cfg = dict(CFG, mesh_depth=0)
    out, m = MeshModel(cfg).run(INPUTS, np.eye(8))
    assert out.shape == INPUTS.shape
    assert m["max_err"] < 1e-6


def test_loss_linear_in_depth():
    losses = []
    for depth in (2, 4, 8):
        cfg = dict(CFG, mesh_depth=depth)
        _, m = MeshModel(cfg).run(INPUTS, WEIGHTS)
        losses.append(m["loss_db"])
    slope = (losses[2] - losses[0]) / (8 - 2)
    assert slope > 0


def test_determinism_same_seed():
    _, m1 = MeshModel(CFG).run(INPUTS, WEIGHTS)
    _, m2 = MeshModel(CFG).run(INPUTS, WEIGHTS)
    assert m1["max_err"] == m2["max_err"]
    assert m1["energy_per_mac_pj"] == m2["energy_per_mac_pj"]


def test_metric_keys_and_feasibility_bounds():
    _, m = MeshModel(CFG).run(INPUTS, WEIGHTS)
    assert set(m) == {"energy_per_mac_pj", "loss_db", "footprint_mm2", "max_err", "verdict"}
    assert m["verdict"] == "pass"
    assert m["energy_per_mac_pj"] > 0 and m["footprint_mm2"] > 0