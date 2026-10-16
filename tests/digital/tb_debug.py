"""Debug TB: per-timestep sim-v vs golden-v state comparison."""

import json
import os

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, Timer

import numpy as np

from targets.digital.model import LIFModel
from targets.digital.rtl_gen import pad_size


@cocotb.test()
async def vtrace(dut):
    cfg = json.loads(os.environ["PARITY_CFG_JSON"])
    steps = int(cfg["timesteps"])
    n = int(cfg["neurons"])
    pad = pad_size(cfg)
    model = LIFModel(cfg)
    train = np.zeros((steps, n), dtype=np.int8)
    train[1::2, 7 % n] = 1

    cocotb.start_soon(Clock(dut.clk, 2, "ns").start())
    dut.rst_n.value = 0
    dut.inject_valid.value = 0
    for _ in range(2):
        await RisingEdge(dut.clk)
    dut.rst_n.value = 1
    await RisingEdge(dut.clk)

    for t in range(steps):
        frame = train[t]
        for s in range(n):
            dut.inject_valid.value = 1
            dut.inject_addr.value = s
            dut.inject_data.value = int(frame[s])
            await RisingEdge(dut.clk)
        dut.inject_valid.value = 0
        await RisingEdge(dut.clk)
        for _ in range(pad + 2):
            await RisingEdge(dut.clk)
            await Timer(1, "ns")
        # read internal v array (icarus VPI supports hierarchical array access)
        sim_v = []
        for i in range(n):
            sim_v.append(int(dut.g_decay[i].v.value.signed_integer))
        model.step(frame)
        dv = np.array(sim_v) - model.get_state_v()
        bad = np.argwhere(dv != 0)
        if bad.size:
            print(f"t={t} v-diff indices={bad.ravel()[:10].tolist()} sim={np.array(sim_v)[bad.ravel()[:10]]} golden={model.get_state_v()[bad.ravel()[:10]]}")
    print("VTRACE DONE")