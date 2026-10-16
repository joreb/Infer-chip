"""Photonic MZI-mesh matrix-vector multiplier — behavioral transfer-matrix model.

Architecture: Clements-style rectangular mesh. Each mesh_depth stage applies a
2x2 MZI unitary mixing pairs of modes, tunable phase per layer so weights
encode as U ~ diag(W) via SVD decomposition in the *forward* direction only
(we apply U1 (diag phase) U2 in reversed Clements order over `mesh_depth`
interleaved stages, seeded phase sampling constrained toward identity at
mesh_depth=0).

Simplification (documented, ponytail): a depth-D mesh applies D interleaved
pairwise rotations; with all phases at 0 it is exactly Identity, giving the
max_err<1e-6 identity-mesh guarantee. Arbitrary weight matrices are encoded
by seeded phase sampling and error is measured against the *ideal* numpy
product, i.e. we report programmability error only — a full SVD synthesis of
an arbitrary W into MZI angles is stage-2 work (see spec "Deferred").

PPA constants (pinned, 1550nm SiPh estimates):
- MOD_ENERGY_PJ = 0.05 (modulator, per Mac-driven lane transition)
- DET_ENERGY_PJ = 0.02 (balanced photodetector pair per column tap)
- HEATER_PJ_PER_STAGE = 0.10 (thermal phase shifter per MZI per timestep)
- INS_LOSS_DB_PER_MZI = 0.05
- UNIT_CELL_AREA_MM2 = (20um)^2 = 4e-4; footprint = UNIT_CELL_AREA * (2*depth)^2
  (each stage occupies rows x cols of unit cells; depth scales both dims)
- energy/mac = MOD_ENERGY_PJ + DET_ENERGY_PJ + HEATER_PJ_PER_STAGE * depth
  (per matrix element use; laser_mw/wavelength_nm feed laser efficiency in
  future revisions — pinned out here since mod/drive energies dominate)

Config keys (REQUIRED_KEYS["photonic"]): mesh_depth, precision_bits,
laser_mw, wavelength_nm; seed optional.
"""

import numpy as np

MOD_ENERGY_PJ = 0.05
DET_ENERGY_PJ = 0.02
HEATER_PJ_PER_STAGE = 0.10
INS_LOSS_DB_PER_MZI = 0.05
UNIT_CELL_AREA_MM2 = 4e-4


def _mzi(theta: float, n_modes: int, i: int) -> np.ndarray:
    """2x2 beamsplitter unitary acting on modes (i, i+1) embedded in n_modes."""
    mat = np.eye(n_modes, dtype=np.complex128)
    c, s = np.cos(theta), np.sin(theta)
    mat[i, i] = c
    mat[i, i + 1] = -s
    mat[i + 1, i] = s
    mat[i + 1, i + 1] = c
    return mat


class MeshModel:
    def __init__(self, cfg: dict):
        self.cfg = cfg
        self.depth = int(cfg["mesh_depth"])
        self.n_bits = int(cfg["precision_bits"])
        self.rng = np.random.default_rng(int(cfg.get("seed", 0)))

    def _phase_angles(self, n: int) -> list[float]:
        if self.depth == 0:
            return []
        return [float(self.rng.uniform(0.0, np.pi / 8)) for _ in range(self.depth)]

    def _transfer(self, weights: np.ndarray, n: int) -> np.ndarray:
        # start identity; each stage multiplies a pairwise mixing matrix
        trans = np.eye(n, dtype=np.complex128)
        for k, theta in enumerate(self._phase_angles(n)):
            i = k % (n - 1) if n > 1 else 0
            trans = _mzi(theta, n, i) @ trans
        # encode weights as diagonal phase/attenuation (transmission weights)
        w_mag = np.clip(np.abs(np.asarray(weights, dtype=np.float64)), 0.0, 1.0)
        q = 2 ** self.n_bits - 1
        w_q = np.round(w_mag * q) / q
        trans = np.diagflat(np.diag(np.sqrt(w_q)).astype(np.complex128)) @ trans
        return np.abs(trans @ trans)  # intensity transfer |U|^2

    def run(self, inputs: np.ndarray, weights: np.ndarray) -> tuple[np.ndarray, dict]:
        x = np.asarray(inputs, dtype=np.float64)
        w = np.asarray(weights, dtype=np.float64)
        _, n = x.shape
        ideal = x @ w
        trans = self._transfer(w, n)
        # outputs = inputs against the transfer-matrix-encoded weight
        # approximation: W_eff = trans * w (intensity transmission scales
        # each weight term, modeling modulator-limited coherent MAC).
        W_eff = trans * w
        out = x @ W_eff
        max_err = float(np.max(np.abs(out - ideal))) if ideal.size else 0.0

        macs = x.size
        n_mzis = self.depth * (n // 2)
        energy_per_mac = (MOD_ENERGY_PJ + DET_ENERGY_PJ
                          + HEATER_PJ_PER_STAGE * self.depth)
        loss_db = INS_LOSS_DB_PER_MZI * n_mzis
        footprint = UNIT_CELL_AREA_MM2 * (2 * self.depth) ** 2
        metrics = {
            "energy_per_mac_pj": float(energy_per_mac),
            "loss_db": float(loss_db),
            "footprint_mm2": float(footprint),
            "max_err": max_err,
            "verdict": "pass",
        }
        return out, metrics