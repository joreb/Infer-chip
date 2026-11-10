---
title: Veryl vs Spade vs Chisel for GPU or core design
created: 2026-10-19
updated: 2026-10-19
type: summary
tags: [hdl, verilog, spade, chisel, veryl, comparison, raw]
sources:
  - wiki/raw/notes/Google - very vs spade vs chisel what to use to build GPU.md
status: open
---

# Veryl vs Spade vs Chisel for GPU or core design

This page summarizes a search note. It compares three HCL/HDL options for a
hardware project such as a GPU.

## Main points

- Verilog is the industry standard. It has broad tool support. It is verbose.
- Chisel is embedded in Scala. It suits large and parameterized designs.
- Spade is a modern Rust-style HDL. It has strong pipeline support.
- Verilog suits fixed-function FPGA work and beginners.
- Chisel suits scalable compute logic and AI designs.
- Spade suits clean pipeline experiments and small modules.
