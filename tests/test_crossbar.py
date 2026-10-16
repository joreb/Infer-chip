"""RRAM crossbar model: physics + PPA metric tests."""

import numpy as np
import pytest

from targets.memristive.crossbar import CrossbarModel

CFG = {
    "xbar_rows": 32,
    "xbar_cols": 32,
    "variability_frac": 0.05,
    "adc_bits": 8,
    "seed": 7,
}

INPUTS = np.asarray(np.random.default_rng(0).random((4, 32)) > 0.7, dtype=np.float64)
WEIGHTS = np.asarray(np.random.default_rng(1).integers(-7, 8, (32, 32)), dtype=np.float64)


def test_zero_inputs_zero_energy():
    out, m = CrossbarModel(CFG).run(np.zeros((4, 32)), WEIGHTS)
    assert m["energy_per_mac_pj"] == 0.0
    assert out.shape == (4, 32)


def test_max_err_monotonic_in_variability():
    errs = []
    for vf in (0.0, 0.05, 0.2):
        cfg = dict(CFG, variability_frac=vf)
        _, m = CrossbarModel(cfg).run(INPUTS, WEIGHTS)
        errs.append(m["max_err"])
    assert errs[0] <= errs[1] <= errs[2]
    assert errs[0] == 0.0  # no variability -> ideal result


def test_determinism_same_seed():
    _, m1 = CrossbarModel(CFG).run(INPUTS, WEIGHTS)
    _, m2 = CrossbarModel(CFG).run(INPUTS, WEIGHTS)
    assert m1["max_err"] == m2["max_err"]


def test_metric_keys_and_verdict():
    _, m = CrossbarModel(CFG).run(INPUTS, WEIGHTS)
    assert set(m) == {"energy_per_mac_pj", "area_mm2", "max_err", "verdict"}
    assert m["verdict"] == "pass"
    assert m["area_mm2"] > 0