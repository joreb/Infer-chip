import subprocess
import sys
from pathlib import Path

from targets.digital.rtl_gen import generate_rtl, module_name

CFG300 = {
    "neurons": 300, "fanout": 8, "weight_width": 4, "timesteps": 32,
    "util_target": 60, "clock_ns": 4.0, "seed": 3,
}
CFG256 = {
    "neurons": 256, "fanout": 8, "weight_width": 4, "timesteps": 32,
    "util_target": 60, "clock_ns": 4.0, "seed": 3,
}


def test_module_name():
    assert module_name(CFG300) == "snn_core_300"


def test_non_pow2_pads_to_next_pow2():
    text = generate_rtl(CFG300)
    assert "module snn_core_300" in text
    assert "module snn_core_512" not in text
    assert "localparam PAD = 512" in text


def test_fixed_ports_present():
    text = generate_rtl(CFG256)
    for port in ("clk", "rst_n", "inject_valid", "inject_addr", "inject_data",
                 "spike_out_valid", "spike_out_addr", "spike_out_data"):
        assert port in text, port


def test_deterministic_identical_weights():
    assert generate_rtl(CFG300) == generate_rtl(CFG300)


def test_iverilog_compiles_256(tmp_path):
    src = tmp_path / "snn_core.v"
    src.write_text(generate_rtl(CFG256))
    out = tmp_path / "out.vp"
    res = subprocess.run(["iverilog", "-tnull", "-o", str(out), str(src)],
                         capture_output=True, text=True)
    assert res.returncode == 0, res.stderr