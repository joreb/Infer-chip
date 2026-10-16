import numpy as np

from targets.digital.model import LIFModel


def test_all_zero_train_returns_all_zero():
    m = LIFModel({"neurons": 8, "fanout": 4, "weight_width": 4, "timesteps": 8})
    out = m.run(np.zeros((8, 8), dtype=np.int8))
    assert out.shape == (8, 8)
    assert not out.any()


def test_single_neuron_hand_computed_trajectory():
    # 1 neuron, weight 1.0 (4-bit int 8 scaled by 1/16). threshold=1.0, decay=0.9.
    m = LIFModel({"neurons": 1, "fanout": 1, "weight_width": 4, "timesteps": 3,
                  "seed": 123, "weights": [[16]]})
    train = np.array([[1], [1], [1]], dtype=np.int8)
    out = m.run(train)
    # step1: v = 0.9*0 + 1.0 = 1.0 -> fire, reset
    # step2: v = 0.9*0 + 1.0 = 1.0 -> fire
    # step3: same
    assert out.tolist() == [[1], [1], [1]]


def test_subthreshold_accumulation_and_decay():
    # Fixed-point arithmetic (T3 ruling): decay = 14/16 truncated, ww=4 lattice.
    m = LIFModel({"neurons": 1, "fanout": 1, "weight_width": 4, "timesteps": 3,
                  "seed": 123, "weights": [[4]]})  # weight 0.25
    train = np.array([[1], [0], [1]], dtype=np.int8)
    out = m.run(train)
    # step1: v = 4/16 = 0.25; step2: (4*14)>>16 = 3/16 = 0.1875; step3: 3+4 = 7/16 = 0.4375
    assert out.tolist() == [[0], [0], [0]]
    np.testing.assert_allclose(m.get_state_v(), [0.4375], rtol=0, atol=1e-12)


def test_determinism_same_seed():
    cfg = {"neurons": 16, "fanout": 4, "weight_width": 4, "timesteps": 32, "seed": 7}
    train = np.random.default_rng(99).integers(0, 2, size=(32, 16)).astype(np.int8)
    a = LIFModel(cfg).run(train)
    b = LIFModel(cfg).run(train)
    assert np.array_equal(a, b)
    assert a.dtype == np.int8 and set(np.unique(a)).issubset({0, 1})


def test_injected_weights_bypass_seeded_sampling():
    # Explicit "weights" cfg key overrides seeded weights (used by RTL parity tests).
    m = LIFModel({"neurons": 2, "fanout": 2, "weight_width": 4, "timesteps": 4,
                  "seed": 5, "weights": [[0, 16], [16, 0]]})
    w = m.get_weights()
    assert w[0][0] == 0.0 and w[1][0] == 1.0