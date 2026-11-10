---
title: Spade spike on one RTL module
created: 2026-10-19
updated: 2026-10-19
type: task
tags: [rtl, architecture, flow]
sources: []
status: done
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

## Evidence gathered (2026-10-19 follow-up)

- Toolchain: Spade 0.20 + swim, iCE40 oss-cad-suite available under
  `~/.local/share/swim/bin/oss-cad-suite/bin`.
- `spikes/spade-lif` builds (`swim build`) and emits `build/spade.sv`.
- Module name is the escaped identifier `\spade_lif_spike::main`; a small
  `wrapper.v` bridges it to a normal top-level (`spade_lif_wrapper`).
- 20,000 randomized input vectors were run through the compiled Verilog
  (`tb_spade.v` + iverilog) and compared bit-for-bit against a Python
  reference reproducing Spade's truncation semantics: **0 mismatches**.
- Arithmetic friction confirmed: each `+`/`-` needs an explicit
  `trunc::<...>`; tuple return packs into a 9-bit word (result in
  bits[8:1], fire in bit 0).
- The spike LIF does not yet mirror the fabric's update: RTL uses a
  wider accumulator (`ACC_W = ww + pad bits + 4`), a dyadic `14/16` decay,
  and no truncation of `v + acc` before compare. Reaching bit-exact against
  the golden model would require widening the Spade module and adding
  decay; the present spike is too narrow.
- Conclusion: for this PoC, RTL authoring stays in Verilog and generation
  stays in Python. Revisit Spade only for Stage 2 agent-authored modules
  where typed port widths earn their keep.

## See also

- [Typed HDL (Stage-2 features checklist, issue #7)](../../index.md)
- [How to run the agent loop](../../tutorials/running-the-agent-loop.md)
