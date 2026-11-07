---
title: Spade spike on one RTL module
created: 2026-10-19
updated: 2026-10-19
type: task
tags: [rtl, architecture, flow]
sources: []
status: open
---

# Spade spike on one RTL module

An open investigation: can one module of the core be authored in Spade,
compiled to Verilog, and verified against the existing golden-model vectors
without disturbing the Python generator or the cocotb bench?

## Candidate module

The LIF update or the weight-pack logic. Both are small, pure functions and
easy to check bit for bit.

## Evidence to gather

- Is a Spade toolchain available and how large is it?
- Does the compiled Verilog drop into the existing cocotb bench unchanged?
- Are the golden-model vectors still passing bit for bit?
- What is the build and debug friction compared with the current Yosys flow?
- Are generics enough for the sizes we need, or does generation stay in Python?

## Decision rule

Proceed to a Stage-2 candidate only if the spike is clean and additive.
Otherwise keep RTL authoring in Verilog and generation in Python.

## See also

- [Typed HDL (Stage-2 features checklist, issue #7)](../../index.md)
- [How to run the agent loop](../../tutorials/running-the-agent-loop.md)
