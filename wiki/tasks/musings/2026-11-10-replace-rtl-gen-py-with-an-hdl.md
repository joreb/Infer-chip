---
title: Replace rtl_gen.py with Amaranth, Veryl, Chisel or Spade
created: 2026-11-10
updated: 2026-11-10
type: musing
tags: [rtl, verification, flow]
sources: []
---

# Replace rtl_gen.py with Amaranth, Veryl, Chisel or Spade

Date: 2026-11-10. Request from JSR: "we should remove rtl gen py with either amarnath/veryl/chisel/spade".
This page reads "amarnath" as [Amaranth HDL](https://amaranth-lang.org/), the Python-embedded HDL.

## Verdict

Remove `targets/digital/rtl_gen.py` and author the LIF fabric in one HDL. The four candidates are
Amaranth, Veryl, Chisel and Spade. This page does not select one. An evaluation selects one
(see "Selection test" below).

This verdict supersedes the PoC decision in `spikes/spade-lif/README.md`: "keep RTL in Verilog and
generation in Python for the PoC; revisit Spade for Stage 2."

## Argument

`targets/digital/rtl_gen.py` (213 lines) writes Verilog text line by line with Python f-strings
(`generate_rtl()` at line 57). This method has these problems:

- No type or width check before Yosys. A width error appears only in simulation or synthesis.
- The generator and the Verilog are two languages in one file. A reader must run the generator to
  see the hardware.
- The text output has no module hierarchy model. Larger designs (for example the 128-lane
  complex unit, GitHub #17) need parameterized modules and generate loops, which an HDL gives
  directly.

Each candidate compiles to Verilog, so ORFS and Yosys stay the same.

| Candidate | Language | Status in this project |
| --- | --- | --- |
| Amaranth | Python library | Not tried. Closest to the current Python code and to the `cfg` dict. |
| Veryl | SystemVerilog-like, Rust toolchain | `spikes/veryl-lif` and `tools/veryl_to_gds.py` gave a GDS with 0 DRC (commit 02a3a6c). |
| Chisel | Scala DSL | Not tried. The sbt install was blocked on 2026-11-08. |
| Spade | Rust-like HDL | `spikes/spade-lif` gave a GDS with 0 DRC (commit 33f244c). Exact-width casts need `trunc::<...>` on each `+` and `-` (GitHub #16). The spike does not have the 14/16 decay and the wide accumulator. |

See [Veryl vs Spade vs Chisel](../../summaries/veryl-vs-spade-vs-chisel.md) for the general comparison.

### What the replacement must keep

These callers import from `rtl_gen.py`. The replacement must supply the same names or the callers
must change:

- `targets/digital/flow.py:16`: `generate_rtl`, `module_name`, `pad_size`
- `targets/digital/evaluate.py:13`: `generate_rtl`, `module_name`, `pad_size`
- `tests/digital/tb_parity.py:24`: `PH_IDLE`, `pad_size`
- `tests/digital/tb_debug.py:13`: `PH_IDLE`, `pad_size`, `weight_words`
- `tests/test_rtl_gen.py`, `tests/test_review_fixes.py`, `tests/digital/test_rtb.py`,
  `tests/digital/gen_debug.py`

The replacement must also keep:

- Bit-exact parity with the golden model in the cocotb bench (`tests/digital/tb_parity.py`).
- The fixed one-cycle SRAM read latency and the external-weight interface.
- The `weight_store = "rom"` variant and its `_rom` module-name suffix.
- `DESIGN_NAME` equal to the generated top module
  ([ENG-007](../../incidents/007-design-name-equals-top-module.md)).

### Selection test

For each candidate, write the full fabric, not one LIF step. Then:

1. Pass `tests/digital/tb_parity.py` bit for bit at 16 and 128 neurons.
2. Run the ORFS flow and compare area, slack and DRC with the `rtl_gen.py` result
   ([PPA metrics](../../tutorials/reading-ppa-metrics.md)).
3. Record install effort, build time and lines of code.

Select the candidate that passes 1 and 2 with the least effort in 3. Delete `rtl_gen.py` only after
the selected design passes all tests.

## Rejection rationale

- Keep Python f-string generation: rejected for the reasons in "Argument".
- Plain hand-written Verilog with parameters: possible, but it gives no type check that is
  stronger than Verilog, and the request names four HDLs.
- Choose one candidate now: rejected. Amaranth and Chisel have no spike in this project, and the
  Spade and Veryl spikes do not cover the full fabric.

## Related

- [Spade spike on one RTL module](../hypothesis/2026-10-19-spade-spike-for-one-module.md)
- [Veryl vs Spade vs Chisel](../../summaries/veryl-vs-spade-vs-chisel.md)
- [From Verilog to a chip layout](../../tutorials/from-verilog-to-gds.md)
- GitHub #7 (Stage-2 backlog, typed HDL item), #16 (Spade spike), #17 (128-lane complex GPU)
