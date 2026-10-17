---
title: RISC-V is a control plane for the SNN fabric, not the fabric itself
created: 2026-10-17
updated: 2026-10-17
type: musing
tags: [architecture, snn, neuromorphic]
sources: []
---

# RISC-V is a control plane for the SNN fabric, not the fabric itself

Date: 2026-10-17. Question: can RISC-V serve as the LLM spiking inference
engine?

## Verdict

RISC-V alone is not a spiking-LLM engine; RISC-V orchestrating the LIF
fabric is. Three integration patterns exist, all silicon-proven, and two
of them fit this repo's architecture without touching the generator or
the verify loop.

## Argument

1. Control plane only (recommended): the core does tokenization, spike
   encoding, address-event routing and SRAM weight streaming; the LIF
   fabric does the neuro-computation. This matches the peer-accepted
   external-SRAM OpenSpike memory interface exactly: RISC-V sequencer,
   LIF array data plane.
2. RISC-V with custom ISA extensions: spike-accumulate/decay instructions
   or a coprocessor on the CV32E40P/CV32E40X X-interface for the
   state-update inner loop.
3. RISC-V as the neuron itself: SpiNNaker2 ships an RV32 core per neuron
   block and each core emulates many LIF neurons. Silicon-proven, but at
   LLM neuron counts it is compute-bound and loses the event-driven
   energy argument — the thesis the fabric exists to test.

Architecture reference for the spiking-LLM line: SpikeGPT (RWKV-style
linear attention, spiking). Its dense matmuls dominate energy; a pure
RISC-V implementation re-serializes exactly the bottleneck the spiking
form exists to avoid.

Core candidates beside our fabric: PicoRV32 if die area is tight on
sky130hs (known PnR success there); CV32E40P for pitch credibility
(production-verified IP).

## Rejection rationale

Pattern 3 conflicts with this project's hardware-fabric thesis. Any
variant that replaces the generator-emitted, parity-verified fabric with
software-executed neurons also orphans the numpy-vs-RTL cocotb proof.

## Related

- [Can one run LLMs on spiking neural network hardware?](2026-10-17-llms-on-snn-hardware.md)
  — the parent question this answer extends.
- [OpenSpike memory interface](../../../docs/openspike-memory-interface.md)
  — the external-SRAM port pattern 1 slots directly onto.
- [ENG-005: ORFS make run is per-stage noop](../../incidents/005-orfs-make-run-is-per-stage-noop.md)
  — the fabric's PnR loop pattern 1 must keep running unchanged.
