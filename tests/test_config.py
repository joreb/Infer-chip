from common.config import REQUIRED_KEYS, estimate_weight_memory_bits, validate_config

BIG = {
    "neurons": 4096,
    "fanout": 1024,
    "weight_width": 8,
    "timesteps": 1024,
    "util_target": 60,
    "clock_ns": 4.0,
}

SANE = {
    "neurons": 256,
    "fanout": 8,
    "weight_width": 4,
    "timesteps": 1024,
    "util_target": 60,
    "clock_ns": 4.0,
}


def test_required_keys_digital():
    assert REQUIRED_KEYS["digital"] == [
        "neurons", "fanout", "weight_width", "timesteps", "util_target", "clock_ns",
    ]


def test_required_keys_other_targets():
    assert REQUIRED_KEYS["photonic"] == [
        "mesh_depth", "precision_bits", "laser_mw", "wavelength_nm",
    ]
    assert REQUIRED_KEYS["memristive"] == [
        "xbar_rows", "xbar_cols", "variability_frac", "adc_bits",
    ]


def test_weight_memory_warning():
    warnings = validate_config("digital", BIG)
    assert any("weight-memory" in w for w in warnings)


def test_sane_weight_memory_no_warning():
    """256 neurons at ww=4 = 0.26 Mbit external SRAM — well inside budget."""
    assert not any("weight-memory" in w for w in validate_config("digital", SANE))


def test_estimate_weight_memory_bits():
    """Dense-by-construction SRAM image: pad words of pad*ww bits; fanout-free."""
    assert estimate_weight_memory_bits({"neurons": 256, "fanout": 8,
                                        "weight_width": 4}) == 262_144
    assert estimate_weight_memory_bits({"neurons": 300, "fanout": 8,
                                        "weight_width": 4}) == 512 * 512 * 4


def test_sane_config_has_no_missing_key_warning():
    warnings = validate_config("digital", SANE)
    assert not any("missing-key" in w for w in warnings)


def test_missing_keys_reported():
    warnings = validate_config("digital", {"neurons": 128})
    assert sum("missing-key" in w for w in warnings) == 5


def test_unknown_target_error():
    import pytest
    with pytest.raises(KeyError):
        validate_config("photon", SANE)