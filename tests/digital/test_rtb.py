"""pytest harness for the cocotb parity testbench (icarus)."""

import json
import os
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[2]

CFG = {
    "neurons": 256, "fanout": 8, "weight_width": 4, "timesteps": 64,
    "util_target": 60, "clock_ns": 4.0, "seed": 11,
}


@pytest.mark.skipif(
    __import__("shutil").which("iverilog") is None, reason="iverilog not installed"
)
def test_sim_parity(tmp_path):
    from targets.digital.rtl_gen import generate_rtl, module_name

    src = tmp_path / "snn_core.v"
    src.write_text(generate_rtl(CFG))

    import cocotb_tools.runner

    runner = cocotb_tools.runner.get_runner("icarus")
    runner.build(
        verilog_sources=[str(src)],
        hdl_toplevel=module_name(CFG),
        build_dir=str(tmp_path / "build"),
    )

    runner.test(
        test_module="tests.digital.tb_parity",
        hdl_toplevel=module_name(CFG),
        build_dir=str(tmp_path / "build"),
        extra_env={
            "PARITY_CFG_JSON": json.dumps(CFG),
            "PYTHONPATH": str(REPO),
        },
    )

@pytest.mark.skipif(
    __import__("shutil").which("iverilog") is None, reason="iverilog not installed"
)
def test_sim_parity_rom_store(tmp_path):
    # dense-ROM baseline (#2) must match the golden model before its PnR
    # numbers mean anything; the TB drives no SRAM in this mode
    from cocotb_tools.check_results import get_results
    import cocotb_tools.runner
    from targets.digital.rtl_gen import generate_rtl, module_name

    cfg = {**CFG, "neurons": 32, "timesteps": 32, "weight_store": "rom"}
    src = tmp_path / "snn_core.v"
    src.write_text(generate_rtl(cfg))
    runner = cocotb_tools.runner.get_runner("icarus")
    runner.build(verilog_sources=[str(src)], hdl_toplevel=module_name(cfg),
                 build_dir=str(tmp_path / "build"))
    xml = runner.test(
        test_module="tests.digital.tb_parity", hdl_toplevel=module_name(cfg),
        build_dir=str(tmp_path / "build"),
        extra_env={"PARITY_CFG_JSON": json.dumps(cfg), "PYTHONPATH": str(REPO)},
    )
    num_tests, num_failed = get_results(Path(xml))
    assert num_tests == 1 and num_failed == 0
