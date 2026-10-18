"""SVD + Clements mesh decomposition and the photonic LIF forward model."""

import numpy as np
import pytest

from targets.digital.model import LIFModel, sample_weight_ints
from targets.photonic.svd_mesh import (clements, mesh_matrix, photonic_lif_run,
                                       svd_program)

CFG = {"neurons": 16, "fanout": 8, "weight_width": 4, "timesteps": 32,
       "util_target": 25, "clock_ns": 40.0}


@pytest.mark.parametrize("n", [2, 5, 16, 128])
def test_clements_reconstructs_a_random_orthogonal_matrix(n):
    q, _ = np.linalg.qr(np.random.default_rng(n).normal(size=(n, n)))
    rots, signs = clements(q)
    assert len(rots) == n * (n - 1) // 2  # one MZI per rotation
    assert np.max(np.abs(mesh_matrix(n, rots, signs) - q)) < 1e-9


def test_svd_program_reconstructs_the_snn_weight_matrix():
    w = sample_weight_ints({**CFG, "neurons": 128})
    prog = svd_program(w)
    assert np.max(prog["sigma"]) == pytest.approx(1.0)  # passive attenuators
    approx = prog["scale"] * mesh_matrix(128, *prog["u"]) @ np.diag(prog["sigma"]) \
        @ mesh_matrix(128, *prog["vt"])
    assert np.max(np.abs(approx - w)) < 1e-9


def _spikes(cfg, seed=0):
    rng = np.random.default_rng(seed)
    return (rng.random((cfg["timesteps"], cfg["neurons"])) < 0.3).astype(np.int8)


def test_ideal_photonic_path_gives_exactly_the_golden_spikes():
    # photonic parity: no noise, no quantization -> same spikes as the golden model
    train = _spikes(CFG)
    golden = LIFModel(CFG).run(train)
    out = photonic_lif_run(CFG, train, phase_bits=None, phase_noise_rad=0.0,
                           laser_mw=None, adc_bits=None)
    assert golden.sum() > 0
    assert np.array_equal(out, golden)


def test_coarse_phases_break_parity():
    # the check must be able to fail: 3-bit phases give wrong spikes
    train = _spikes(CFG)
    golden = LIFModel(CFG).run(train)
    out = photonic_lif_run(CFG, train, phase_bits=3, phase_noise_rad=0.0,
                           laser_mw=None, adc_bits=None)
    assert not np.array_equal(out, golden)


def test_laser_power_changes_accuracy():
    # issue #6: laser_mw must have an effect; less light -> more detector noise
    cfg = {**CFG, "neurons": 32, "timesteps": 64}
    train = _spikes(cfg)
    golden = LIFModel(cfg).run(train)
    errs = [np.mean(photonic_lif_run(cfg, train, phase_bits=None, phase_noise_rad=0.0,
                                     laser_mw=p, adc_bits=None, seed=1) != golden)
            for p in (0.01, 100.0)]
    assert errs[0] > errs[1]
