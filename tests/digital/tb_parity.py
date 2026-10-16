"""cocotb testbench: sim-vs-golden LIF parity.

Protocol per rtl_gen docstring: P inject cycles per timestep (valid=1,
addr=source, data=bit) then one boundary cycle (valid=0), then an emission
window of PAD+2 cycles collecting spike_out events. Pins both Task-3/4
Review Focus inputs: all-zero frames and the deterministic pattern run
through the same golden-model weights (same seed).
"""

import json
import os

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, Timer

import numpy as np

from targets.digital.model import LIFModel
from targets.digital.rtl_gen import pad_size


def _frames(cfg: dict) -> np.ndarray:
    """Alternating all-zero / fixed 3-spike frames, [T, N] int8."""
    steps = int(cfg["timesteps"])
    n = int(cfg["neurons"])
    train = np.zeros((steps, n), dtype=np.int8)
    train[1::2, [7 % n, 8 % n, 9 % n]] = 1
    return train


@cocotb.test()
async def parity(dut):
    cfg = json.loads(os.environ["PARITY_CFG_JSON"])
    steps = int(cfg["timesteps"])
    n = int(cfg["neurons"])
    pad = pad_size(cfg)
    model = LIFModel(cfg)
    train = _frames(cfg)

    cocotb.start_soon(Clock(dut.clk, 2, "ns").start())
    dut.rst_n.value = 0
    dut.inject_valid.value = 0
    dut.inject_addr.value = 0
    dut.inject_data.value = 0
    for _ in range(2):
        await RisingEdge(dut.clk)
    dut.rst_n.value = 1
    await RisingEdge(dut.clk)

    out = np.zeros((steps, n), dtype=np.int8)
    for t in range(steps):
        frame = train[t]
        for s in range(pad):
            dut.inject_valid.value = 1
            dut.inject_addr.value = s
            dut.inject_data.value = int(frame[s])
            await RisingEdge(dut.clk)
        dut.inject_valid.value = 0
        dut.inject_data.value = 0
        await RisingEdge(dut.clk)  # boundary: last contribution lands, UPDATE next
        for _ in range(pad + 2):
            await RisingEdge(dut.clk)
            await Timer(1, "ns")  # settle NBA before reading outputs
            if int(dut.spike_out_valid.value) == 1:
                out[t][int(dut.spike_out_addr.value)] = int(dut.spike_out_data.value)

    expected = model.run(train)
    mismatches = np.argwhere(out != expected)
    assert not mismatches.size, (
        f"{mismatches.size} timestep/neuron mismatches; first at "
        f"t={mismatches[0][0]} neuron={mismatches[0][1]}: "
        f"sim={out[tuple(mismatches[0])]} golden={expected[tuple(mismatches[0])]}"
    )
    # sanity: fires actually occurred somewhere
    assert expected.sum() > 0, "pattern produced no spikes; test would be vacuous"