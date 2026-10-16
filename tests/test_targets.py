"""Target registry + evaluate contract tests."""

import numpy as np
import pytest

from targets.base import get_target


def test_registry_lookup():
    assert get_target("digital").name == "digital"
    assert get_target("photonic").name == "photonic"
    assert get_target("memristive").name == "memristive"


def test_registry_unknown_raises():
    with pytest.raises(KeyError):
        get_target("nope")


def test_photonic_evaluate_contract(tmp_path):
    cfg = {
        "mesh_depth": 4, "precision_bits": 8, "laser_mw": 1.0,
        "wavelength_nm": 1550, "seed": 3,
    }
    out = get_target("photonic").evaluate(cfg, tmp_path)
    assert set(out) == {"sim", "flow", "config"}
    assert out["sim"]["verdict"] == "pass"
    assert out["flow"]["verdict"] == "pass"
    assert out["config"] == cfg


def test_memristive_evaluate_contract(tmp_path):
    cfg = {
        "xbar_rows": 32, "xbar_cols": 32, "variability_frac": 0.05,
        "adc_bits": 8, "seed": 7,
    }
    out = get_target("memristive").evaluate(cfg, tmp_path)
    assert out["sim"]["verdict"] == "pass"
    assert out["flow"]["verdict"] == "pass"
    assert isinstance(out["flow"]["energy_per_mac_pj"], float)


def test_digital_evaluate_sim_fail_short_circuits_flow(tmp_path, monkeypatch):
    import targets.digital.evaluate as de
    monkeypatch.setattr(de.DigitalTarget, "_run_sim", lambda self, cfg, out_dir: {"verdict": "fail", "reason": "boom"})
    cfg = {
        "neurons": 8, "fanout": 2, "weight_width": 4, "timesteps": 8,
        "util_target": 60, "clock_ns": 4.0, "seed": 11,
    }
    out = de.DigitalTarget().evaluate(cfg, tmp_path)
    assert out["sim"]["verdict"] == "fail"
    assert out["flow"] == {"verdict": "skipped", "reason": "sim failed"}


def test_digital_evaluate_pass_runs_flow(tmp_path, monkeypatch):
    import targets.digital.evaluate as de
    monkeypatch.setattr(de.DigitalTarget, "_run_sim", lambda self, cfg, out_dir: {"verdict": "pass", "fires": 3})
    monkeypatch.setattr(de.DigitalTarget, "_run_flow", lambda self, cfg, out_dir: {"verdict": "pass", "area_mm2": 0.03})
    cfg = {
        "neurons": 8, "fanout": 2, "weight_width": 4, "timesteps": 8,
        "util_target": 60, "clock_ns": 4.0, "seed": 11,
    }
    out = de.DigitalTarget().evaluate(cfg, tmp_path)
    assert out["flow"]["verdict"] == "pass"
    assert out["flow"]["area_mm2"] == 0.03