"""Golden LIF reference model — the truth the RTL must match, bit-exact.

Synapse topology: neuron i receives from `fanout` presynaptic sources drawn
with the same seeded rng the RTL generator uses (pre-flight ruling T2->T4),
so the cocotb testbench can build an identical model. An explicit "weights"
config key ([N][N] ints/floats) overrides sampling.

Task-3 ruling: all arithmetic is integer fixed-point at weight_width scale so
the cocotb sim-vs-golden parity is bit-exact. Float inputs (threshold, rest,
leak) are quantized to the ww lattice; decay is a dyadic 14/16 (= 0.875)
implemented as truncating shift, identical to RTL.
"""

import numpy as np

DECAY_NUM = 14
DECAY_SHIFT = 4
NEURON_DEFAULTS = {"threshold": 1.0, "rest": 0.0, "leak": 0.0}


def sample_weight_ints(cfg: dict) -> np.ndarray:
    """Sparse int weight matrix [N, N]: <=fanout nonzero sources per row.

    Integers in +/-(2**weight_width - 1); RTL emits these verbatim, the golden
    model divides by 2**weight_width. An explicit "weights" cfg key (ints or
    floats, [N][N]) overrides sampling (scaled by 2**ww back to ints).
    """
    n = int(cfg["neurons"])
    fanout = min(int(cfg["fanout"]), n)
    ww = int(cfg["weight_width"])
    rng = np.random.default_rng(cfg.get("seed", 1))
    w = np.zeros((n, n), dtype=np.int64)
    w_int_max = 2**ww - 1
    if "weights" in cfg:
        # cfg "weights" are already integer-lattice values (weight * 2**ww),
        # same convention the sampled ints and the RTL ROM use.
        w = np.rint(np.asarray(cfg["weights"], dtype=np.float64)).astype(np.int64)
    else:
        for i in range(n):
            srcs = rng.choice(n, size=fanout, replace=False)
            vals = rng.integers(-w_int_max, w_int_max + 1, size=fanout)
            w[i, srcs] = vals
    return w


def sample_weights(cfg: dict) -> np.ndarray:
    """Float view of the sampled weights (golden model / report use)."""
    return sample_weight_ints(cfg) / 2 ** int(cfg["weight_width"])


class LIFModel:
    def __init__(self, cfg: dict):
        self.cfg = cfg
        self.n = int(cfg["neurons"])
        self.ww = int(cfg["weight_width"])
        self.scale = 2**self.ww
        self.decay_num = DECAY_NUM  # dyadic; matches RTL shift
        self.decay_shift = DECAY_SHIFT
        self.rest = int(round(float(cfg.get("rest", NEURON_DEFAULTS["rest"])) * self.scale))
        self.leak = int(round(float(cfg.get("leak", NEURON_DEFAULTS["leak"])) * self.scale))
        self.threshold = int(round(float(cfg.get("threshold", NEURON_DEFAULTS["threshold"])) * self.scale))
        self.w = sample_weight_ints(cfg)
        self.v = np.full(self.n, self.rest, dtype=np.int64)

    def get_weights(self) -> np.ndarray:
        """Float view of weights."""
        return self.w / self.scale

    def get_weights_int(self) -> np.ndarray:
        return self.w

    def get_state_v(self) -> np.ndarray:
        """Float view of membrane state."""
        return self.v / self.scale

    def step(self, spikes: np.ndarray) -> np.ndarray:
        """One timestep: v' = (decay*v + W@s - leak) in ww-scale ints; fire >= threshold."""
        s = np.asarray(spikes).reshape(-1)
        current = self.w @ s[: self.n]
        v = ((self.decay_num * self.v) >> self.decay_shift) + current - self.leak
        fires = v >= self.threshold
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