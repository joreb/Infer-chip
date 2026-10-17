---
title: Why not hls4ml for the fabric itself?
created: 2026-10-17
updated: 2026-10-17
type: musing
tags: [hls, rtl, verification]
sources: []
---

# Why not hls4ml for the fabric itself?

Date: 2026-10-17. Question asked by JSR during the digital e2e PnR run:
"why use rtl_gen.py, why not hls4ml?" Short answer: the block is an
event-driven LIF fabric, not an inference graph.

## What hls4ml is for

Compiling quantized ANN inference graphs (Keras/ONNX: dense, conv, pooling,
activations) into HLS and then RTL. Matmul-heavy, frame-based, scheduled
dataflow pipelines.

## Why it fights this block

1. No SNN semantics. Membrane state machine (decay, integrate, threshold,
   reset), spike-event in and out, time-binned accumulation: none of that is
   an hls4ml primitive. We would write custom HLS C++ for the entire core,
   erasing most of the benefit of the mature layer library.

2. Wrong shape. The fabric is a streaming FSM with an OpenSpike SRAM port
   (no handshake, fixed latency) and a PAD+O(1) cycle budget per timestep.
   hls4ml's model is weights inside the design as ROMs, scheduled dataflow.
   The peer-accepted architecture is the opposite: weights external, fabric
   protocol-conformant, cycle budget a design property asserted in a test.

3. Verification loop. The cocotb bit-exact parity against the numpy golden
   model pins the RTL per config. HLS adds Vitis or Catapult compile cycles
   and a second source of truth; Catapult is closed and licensed.

4. Pitch honesty. The OpenSpike cycle comparison (about 272 cycles per
   timestep at 256 neurons) only works as a pitch number when the schedule
   is visible. An opaque HLS pipeline hides the timing budget behind tool
   pragmatics.

## Where hls4ml does earn a place

A dense quantized-ANN baseline or an ANN front-end beside the SNN core.
Onnx import nearly free, layer libraries mature. Stage 2, additive, not a
replacement. Recorded in docs/backlog.md entry 2.

## The agent framing clinches it

The one-loop claim rests on "agent picks configs over a deterministic,
verified generator". rtl_gen.py is about 180 lines of pure Python,
deterministic per seed, parity-checked on every run. Swapping it moves the
complexity from transparent generated text to opaque tool behavior, right
before a jury pitch, for no hardware story we do not already have.

## Related

- [BindSNET for model gen and hls4ml for RTL?](2026-10-17-bindsnet-plus-hls4ml-seam.md)
- [BindSNET is a trainer, not a golden model](2026-10-17-bindsnet-not-a-golden-model.md)
- [Wiki index](../../index.md)
