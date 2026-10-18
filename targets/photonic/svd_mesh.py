"""SVD + Clements MZI mesh for the SNN weight matrix, and its LIF forward model.

The digital core computes I = W @ s each timestep (W: N x N signed ints, s:
binary spikes). A photonic core does the same product optically:

    W = scale * U @ diag(sigma) @ Vt,  sigma <= 1 (passive attenuators)

U and Vt are real orthogonal, so each is a rectangular (Clements) mesh of
N(N-1)/2 Givens rotations (one 2x2 MZI each) plus a +-1 sign column. The
input spikes drive one modulator per mode, the output is read with coherent
detection (signed field amplitude, needs a phase reference), then the
electronic gain `scale` and the integer LIF update are digital.

Non-idealities modelled: phase quantization, Gaussian phase noise, and
detector noise set by the laser power after insertion loss. Constants marked
ASSUMED are not from a measured device; the plots sweep them.

Clements, Humphreys, Metcalf, Kolthammer, Walmsley, "Optimal design for
universal multiport interferometers", Optica 3(12) 2016, arXiv 1603.08788.
"""

import numpy as np

from targets.digital.model import LIFModel, sample_weight_ints

INS_LOSS_DB_PER_MZI = 0.1   # ASSUMED, swept in the plots
P_NOISE_MW = 1e-6           # ASSUMED detector noise power (1 nW) in the signal band


def _rotate(m: np.ndarray, k: int, theta: float, rows: bool = True) -> None:
    """In place: Givens rotation [[c, -s], [s, c]] on rows (or columns) k, k+1."""
    c, s = np.cos(theta), np.sin(theta)
    if rows:
        a, b = m[k].copy(), m[k + 1].copy()
        m[k], m[k + 1] = c * a - s * b, s * a + c * b
    else:
        a, b = m[:, k].copy(), m[:, k + 1].copy()
        m[:, k], m[:, k + 1] = c * a + s * b, -s * a + c * b


def clements(q: np.ndarray) -> tuple[list[tuple[int, float]], np.ndarray]:
    """Real orthogonal q -> (rotations in light order, output signs).

    mesh_matrix(n, rots, signs) == q. Nulling order of Clements et al. 2016;
    the +-1 diagonal is pushed through the left-side rotations to the output.
    """
    u = np.array(q, dtype=np.float64)
    n = u.shape[0]
    left, right = [], []
    for i in range(n - 1):
        if i % 2 == 0:
            for j in range(i + 1):
                r, k = n - 1 - j, i - j
                theta = np.arctan2(-u[r, k], u[r, k + 1])
                _rotate(u, k, theta, rows=False)   # u @ G
                right.append((k, theta))
        else:
            for j in range(1, i + 2):
                r, c = n + j - i - 2, j - 1
                theta = np.arctan2(-u[r, c], u[r - 1, c])
                _rotate(u, r - 1, theta)           # G @ u
                left.append((r - 1, theta))
    d = np.sign(np.diag(u))
    # q = L^T D R^T: light sees R^T first, then D, then L^T; G^T(t) = G(-t)
    rots = [(k, -t) for k, t in right]
    for k, t in reversed(left):
        rots.append((k, -t if d[k] == d[k + 1] else t))  # G(p) D = D G(+-p)
    return rots, d


def mesh_matrix(n: int, rots, signs) -> np.ndarray:
    m = np.eye(n)
    for k, t in rots:
        _rotate(m, k, t)
    return np.asarray(signs)[:, None] * m


def svd_program(w: np.ndarray) -> dict:
    u, s, vt = np.linalg.svd(np.asarray(w, dtype=np.float64))
    return {"u": clements(u), "vt": clements(vt), "sigma": s / s[0], "scale": float(s[0])}


def _quant(theta: float, bits: int | None) -> float:
    if bits is None:
        return theta
    step = 2 * np.pi / 2 ** bits
    return float(np.round(theta / step) * step)


def realized_matrix(prog: dict, n: int, phase_bits, phase_noise_rad, rng) -> np.ndarray:
    def mesh(rots, signs):
        return mesh_matrix(n, [(k, _quant(t, phase_bits) + rng.normal(0, phase_noise_rad)
                                if phase_noise_rad else _quant(t, phase_bits))
                               for k, t in rots], signs)
    # attenuator i is an MZI at angle arccos(sigma_i): same phase errors apply
    alpha = np.arccos(np.clip(prog["sigma"], 0, 1))
    sig = np.cos([_quant(a, phase_bits) + (rng.normal(0, phase_noise_rad) if phase_noise_rad else 0)
                  for a in alpha])
    return prog["scale"] * mesh(*prog["u"]) @ np.diag(sig) @ mesh(*prog["vt"])


def photonic_lif_run(cfg: dict, train: np.ndarray, phase_bits=None, phase_noise_rad=0.0,
                     laser_mw=None, adc_bits=None, seed: int = 0) -> np.ndarray:
    """Photonic W @ s, then the same integer LIF update as the golden model."""
    rng = np.random.default_rng(seed)
    n = int(cfg["neurons"])
    prog = svd_program(sample_weight_ints(cfg))
    a = realized_matrix(prog, n, phase_bits, phase_noise_rad, rng)
    full_scale = prog["scale"] * np.sqrt(n)  # |A s| <= scale * |s| <= scale * sqrt(n)
    sigma_n = 0.0
    if laser_mw is not None:
        loss_db = INS_LOSS_DB_PER_MZI * (2 * n + 1)  # two meshes + attenuator per path
        p_rx = laser_mw / n * 10 ** (-loss_db / 10)
        sigma_n = full_scale * np.sqrt(P_NOISE_MW / p_rx)
    ref = LIFModel(cfg)  # parameters only; the golden model stays untouched
    v = np.full(n, ref.rest, dtype=np.int64)
    out = np.zeros(train.shape, dtype=np.int8)
    for t, s in enumerate(np.asarray(train)):
        cur = a @ s[:n] + (rng.normal(0, sigma_n, n) if sigma_n else 0)
        if adc_bits is not None:
            lsb = 2 * full_scale / 2 ** adc_bits
            cur = np.round(cur / lsb) * lsb
        cur = np.rint(cur).astype(np.int64)
        v = ((ref.decay_num * v) >> ref.decay_shift) + cur - ref.leak
        fire = v >= ref.threshold
        v[fire] = ref.rest
        out[t] = fire
    return out
