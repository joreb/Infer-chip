"""Golden numpy LIF reference model — the truth the RTL must match.

Synapse topology: neuron i receives from `fanout` presynaptic sources drawn
with the same seeded rng the RTL generator uses (pre-flight ruling T2->T4),
so the cocotb testbench can build an identical model. An explicit "weights"
config key ([N][N] ints/floats) overrides sampling.
"""

import numpy as np

NEURON_DEFAULTS = {"threshold": 1.0, "decay": 0.9, "rest": 0.0, "leak": 0.0}


def sample_weights(cfg: dict) -> np.ndarray:
    """Sparse int-scaled weight matrix [N, N]: <=fanout nonzero sources per row.

    Integers in +/-(2**weight_width - 1), scaled by 1/2**weight_width, so the
    RTL generator can emit the exact same values as fixed-point synapse rows.
    """
    n = int(cfg["neurons"])
    fanout = min(int(cfg["fanout"]), n)
    ww = int(cfg["weight_width"])
    rng = np.random.default_rng(cfg.get("seed", 1))
    w = np.zeros((n, n), dtype=np.int32)
    w_int_max = 2**ww - 1
    for i in range(n):
        srcs = rng.choice(n, size=fanout, replace=False)
        vals = rng.integers(-w_int_max, w_int_max + 1, size=fanout, dtype=np.int32)
        w[i, srcs] = vals
    return w.astype(np.float64) / 2**ww


class LIFModel:
    def __init__(self, cfg: dict):
        self.cfg = cfg
        for k, v in NEURON_DEFAULTS.items():
            setattr(self, k, float(cfg.get(k, v)))
        self.n = int(cfg["neurons"])
        if "weights" in cfg:
            # Fixed-point ints, same convention as sampling: scaled by 1/2**weight_width.
            self.w = np.asarray(cfg["weights"], dtype=np.float64) / 2**int(cfg["weight_width"])
        else:
            self.w = sample_weights(cfg)
        self.v = np.full(self.n, self.rest)

    def get_weights(self) -> np.ndarray:
        return self.w

    def get_state_v(self) -> np.ndarray:
        return self.v.copy()

    def step(self, spikes: np.ndarray) -> np.ndarray:
        """One timestep: v' = decay*(v - rest) + W@s - leak; fire >= threshold."""
        s = np.asarray(spikes, dtype=np.float64).reshape(-1)
        current = self.w @ s
        v = self.decay * (self.v - self.rest) + current - self.leak
        fires = (v >= self.threshold)
        v[fires] = self.rest
        self.v = v
        return fires.astype(np.int8)

    def run(self, spike_train: np.ndarray) -> np.ndarray:
        """Run [T, N] injected spike train -> [T, N] emitted spikes."""
        train = np.asarray(spike_train)
        out = np.zeros(train.shape, dtype=np.int8)
        for t in range(train.shape[0]):
            out[t] = self.step(train[t])
        return out