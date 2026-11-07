---
title: Evaluate building an FPGA prototype for the spiking core
created: 2026-10-19
updated: 2026-10-19
type: task
tags: [architecture, flow, snn]
sources: []
status: open
---

# Evaluate building an FPGA prototype for the spiking core

This task records an open evaluation: should we build an FPGA prototype of the
spiking core before the 2026-11-30 pitch?

## Question

Is it worth building an FPGA prototype of `snn_core` for the pitch demo, given
the Yosys resource estimate and the bring-up cost already noted in the robot
integration musing?

## What is already known

The [robot integration musing](../musings/2026-10-19-edge-robot-integration-spi-not-pcie.md)
estimates about 9.9k LUT and 128 DSP on Xilinx 7-series, or 9.1k LUT4 and 128
MULT18 on ECP5. The core fits a small FPGA once the LIF decay multiply is made
DSP-free. The musing also budgets a QSPI link and a 1 ms control loop.

## Evidence to gather

- Does `snn_core` synthesise clean on a target FPGA with zero timing violations?
- What board and programmer hardware is needed, and what is the lead time?
- How much effort is QSPI bring-up and parity testing against the RTL golden model?
- How much extra weight memory and I/O does the prototype need beyond the core?
- Does the prototype improve the pitch story enough to justify that effort?

## Decision rule

Proceed only if the prototype adds a runnable demonstration without delaying the
silicon tape-out narrative or the verified RTL to PnR path. Otherwise keep it
as a Stage-2 item.

## See also

- [FPGA prototype and robot interface (issue #13)](../../index.md) for the tracking issue
- [How to run the agent loop](../../tutorials/running-the-agent-loop.md) for evidence recording
