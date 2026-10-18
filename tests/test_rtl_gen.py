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
    for port in ("clk", "rst_n", "timestep_start", "in_spk", "w_read_sram",
                 "w_read_sram_addr", "spike_out_valid", "spike_out_addr",
                 "spike_out_data"):
        assert port in text, port


def test_no_embedded_weight_memory():
    """Weights are external (docs/openspike-memory-interface.md): no dense ROM."""
    text = generate_rtl(CFG256)
    assert "rom_word" not in text
    assert "function" not in text  # the old case-tree ROM function is gone


def test_deterministic_identical_weights():
    assert generate_rtl(CFG300) == generate_rtl(CFG300)


def test_iverilog_compiles_256(tmp_path):
    src = tmp_path / "snn_core.v"
    src.write_text(generate_rtl(CFG256))
    out = tmp_path / "out.vp"
    res = subprocess.run(["iverilog", "-tnull", "-o", str(out), str(src)],
                         capture_output=True, text=True)
    assert res.returncode == 0, res.stderr

ROM16 = {"neurons": 16, "fanout": 4, "weight_width": 4, "timesteps": 16,
         "util_target": 25, "clock_ns": 40.0, "seed": 3, "weight_store": "rom"}


def test_rom_store_holds_the_same_weight_words_on_die():
    # dense-ROM baseline (#2): same FSM, the SRAM port moves inside as a
    # constant case tree filled from the TB's SRAM image
    from targets.digital.model import weight_words
    text = generate_rtl(ROM16)
    assert module_name(ROM16) == "snn_core_16_rom"
    assert "module snn_core_16_rom" in text
    assert "input  wire [64-1:0] w_read_sram" not in text
    assert "output reg  [5-1:0] w_read_sram_addr" not in text
    # registered read keeps the addr-in-N, data-in-N+1 latency
    assert "w_read_sram <= rom_word(w_read_sram_addr);" in text
    for s, w in enumerate(weight_words(ROM16)):
        assert f"5'd{s}: rom_word = 64'h{w:016x};" in text


def test_external_store_is_the_default():
    assert module_name(CFG256) == "snn_core_256"
    assert "rom_word" not in generate_rtl({**CFG256, "weight_store": "external"})


def test_iverilog_compiles_rom(tmp_path):
    src = tmp_path / "snn_core.v"
    src.write_text(generate_rtl(ROM16))
    res = subprocess.run(["iverilog", "-tnull", "-o", str(tmp_path / "o"), str(src)],
                         capture_output=True, text=True)
    assert res.returncode == 0, res.stderr
