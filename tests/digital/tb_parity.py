"""cocotb testbench: sim-vs-golden LIF parity over the OpenSpike memory interface.

The fabric holds no weight memory (docs/openspike-memory-interface.md). The
TB models external SRAM: synchronously sampled, registered address output,
address stable in cycle N -> data on w_read_sram in cycle N+1, no handshake.

Per timestep the host drives one in_spk frame and pulses timestep_start; the
fabric streams all PAD weight words itself and emits fires on spike_out_*
until it returns to IDLE. Also pins the fixed cycle budget (independent of
spike rate): RUN lasts PAD+2 edges, so a timestep costs PAD+3 edges plus one
edge per emitted fire.
"""

import json
import os

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, Timer

import numpy as np

from targets.digital.model import LIFModel, weight_words
from targets.digital.rtl_gen import PH_IDLE, pad_size


def _frames(cfg: dict) -> np.ndarray:
    """Alternating all-zero / fixed 3-spike frames, [T, N] int8."""
    steps = int(cfg["timesteps"])
    n = int(cfg["neurons"])
    train = np.zeros((steps, n), dtype=np.int8)
    train[1::2, [7 % n, 8 % n, 9 % n]] = 1
    return train


async def _run_timestep(dut, frame, n, pad, out_t):
    """Latch one frame via timestep_start, wait for IDLE, collect emissions.

    Writes fired addresses into out_t; returns edges elapsed from the start
    pulse to the IDLE return.
    """
    spikes = sum(int(frame[s]) << s for s in range(n))
    dut.in_spk.value = spikes
    dut.timestep_start.value = 1
    await RisingEdge(dut.clk)  # IDLE edge latches frame + zeroes SRAM addr
    dut.timestep_start.value = 0
    cycles = 0
    while True:
        await RisingEdge(dut.clk)
        await Timer(1, "ns")  # settle NBA before reading outputs/phase
        cycles += 1
        if int(dut.spike_out_valid.value) == 1:
            out_t[int(dut.spike_out_addr.value)] = int(dut.spike_out_data.value)
        if int(dut.phase.value) == PH_IDLE:
            return cycles


@cocotb.test()
async def parity(dut):
    cfg = json.loads(os.environ["PARITY_CFG_JSON"])
    steps = int(cfg["timesteps"])
    n = int(cfg["neurons"])
    pad = pad_size(cfg)
    model = LIFModel(cfg)
    train = _frames(cfg)
    words = weight_words(cfg)
    # weight_store=rom (#2): the weights are on die, the TB drives no SRAM
    ext = cfg.get("weight_store", "external") != "rom"

    # external weight SRAM: registered read, addr in cycle N -> data in N+1
    async def sram():
        while True:
            await RisingEdge(dut.clk)
            a = int(dut.w_read_sram_addr.value)
            if a < pad:
                dut.w_read_sram.value = words[a]

    cocotb.start_soon(Clock(dut.clk, 2, "ns").start())
    dut.rst_n.value = 0
    dut.timestep_start.value = 0
    dut.in_spk.value = 0
    if ext:
        dut.w_read_sram.value = 0
    for _ in range(2):
        await RisingEdge(dut.clk)
    dut.rst_n.value = 1
    await RisingEdge(dut.clk)
    if ext:
        cocotb.start_soon(sram())

    out = np.zeros((steps, n), dtype=np.int8)
    for t in range(steps):
        cycles = await _run_timestep(dut, train[t], n, pad, out[t])
        # fixed budget: RUN(PAD+2) + UPDATE(1) + EMIT(fires) + IDLE return;
        # pad+3 + (n fires worst case) + slack, independent of spike rate
        assert cycles <= pad + 4 + n, f"t={t}: timestep took {cycles} cycles"

    expected = model.run(train)
    mismatches = np.argwhere(out != expected)
    assert not mismatches.size, (
        f"{mismatches.size} timestep/neuron mismatches; first at "
        f"t={mismatches[0][0]} neuron={mismatches[0][1]}: "
        f"sim={out[tuple(mismatches[0])]} golden={expected[tuple(mismatches[0])]}"
    )
    # sanity: fires actually occurred somewhere
    assert expected.sum() > 0, "pattern produced no spikes; test would be vacuous"