---
title: For a robot arm, use an FPGA prototype on a SPI daughterboard, not a PCIe board
created: 2026-10-19
updated: 2026-10-19
type: musing
tags: [snn, neuromorphic, architecture]
sources: []
---

# For a robot arm, use an FPGA prototype on a SPI daughterboard, not a PCIe board

Text written in ASD-STE100 Simplified Technical English.

Date: 2026-10-19. Question asked by JSR: "If I want to run it AI-native for a robotic platform and
edge AI, why would I use my PC? Should I set it up as a PCIe board, so that the device can go on
another board of a robotic arm?" Feature issue: GitHub #13.

## Verdict

Do not make the core a PCIe board. Put it on a small daughterboard with a QSPI interface to the
arm controller. Build it first on an FPGA, because no silicon exists yet. The PC stays the design
machine. It is not part of the robot.

## Argument

1. **The PC is the design tool, not the robot computer.** "AI-native" in this project means that an
   AI agent designs the chip. The PC runs the flow, the simulation and the agent. On the robot, only
   the finished core runs.
2. **The core needs little bandwidth.** At the 40 ns clock, one timestep takes 5.29 µs, and its input
   is 128 bits. That is about 24 Mbit/s at full speed. QSPI at 50 MHz gives 200 Mbit/s. PCIe gives
   gigabits per second, so the core would use about 1% of it. These values are derived from the
   measured 128-neuron run, see [performance plots](../../summaries/128-neuron-core-performance.md).
3. **The control loop needs a short, constant latency, not bandwidth.** A joint control loop
   typically runs at 1 kHz. With 64 timesteps per control cycle, the expected time is about 0.39 ms:
   41 µs to send the frames, 339 µs to compute, and a few µs to read the spikes. A simple SPI link
   has a fixed timing, which makes this budget easy to keep.
4. **sky130 and the open flow cannot make PCIe.** PCIe needs high-speed transceivers. The sky130 I/O
   pins are slow, and the open flow has no PCIe PHY.
5. **Robot arm controllers speak SPI, CAN and UART.** They are microcontrollers or embedded boards
   (for example a Jetson or a Raspberry Pi Compute Module). A SPI daughterboard connects to all of
   them.
6. **An FPGA runs the same Verilog now.** Yosys synthesis of the 128-neuron core gives about 9.9k
   LUTs and 128 DSP blocks on Xilinx 7-series, and about 9.1k LUT4s and 128 multipliers on ECP5,
   without the weight memory (measured 2026-10-18, synthesis only). The 128 DSP blocks come from the
   `v * 14` decay. A shift-and-subtract version removes them, so a small FPGA is sufficient.

## Rejection rationale

| Option | Why rejected now |
|---|---|
| PCIe card | Needs transceivers and a PC-class host. 100 times more bandwidth than necessary. Not possible in sky130. Good only for an FPGA card in the design PC |
| USB | Full-speed USB polls each 1 ms, which is the full control-loop budget. Latency jitter is hard to control |
| Ethernet or EtherCAT | Good for industrial arms later. Too much logic and protocol for the first prototype |
| Wait for silicon | A tapeout takes months. The FPGA gives a demo before the pitch on 2026-11-30 |

## How the parts fit

```text
design time:  PC (agent loop, ORFS, simulation)  ->  Verilog + GDS
run time:     arm controller (MCU or embedded board)
                 |  QSPI + IRQ, 3.3 V
              daughterboard: FPGA (later: sky130 chip)
                 core + weight BRAM (#11) + optional RISC-V controller (#12)
```

The LLM agent of the [experience-memory musing](2026-10-18-snn-experience-memory-for-calibration.md)
runs on the embedded board or off the robot. It must not be in the real-time loop.

## Related

- GitHub #13 (this feature), #11 (loadable weights), #12 (RISC-V control processor)
- [Weight storage hierarchy](../../concepts/weight-storage-hierarchy.md)
- [RISC-V is a control plane](2026-10-17-riscv-is-control-plane-not-the-fabric.md)
- [index](../../index.md)
