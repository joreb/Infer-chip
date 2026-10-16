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