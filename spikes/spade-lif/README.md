# Spade spike for one LIF update

Scoped, additive experiment referenced by issue #16 and the Typed HDL
backlog item. It does **not** replace the Python generator or the cocotb
bench.

- Source: `src/main.spade`
- Build: `swim build`
- Synthesis check: `swim synth` (requires yosys in PATH via oss-cad-suite)

The module compiles and synthesizes to 42 `SB_LUT4` + 15 `SB_CARRY` on
the iCE40 flow per the original run. The main friction is Spade's
exact-width arithmetic: each `+` / `-` needs an explicit
`trunc::<...>` rather than automatic widening.

Follow-up verification (2026-10-19): `build/spade.sv` plus a thin
`wrapper.v` (escaped module name `\\spade_lif_spike::main`) compiles under
iverilog. `tb_spade.v` drives 20,000 randomized input vectors and the
simulated output matches a Python reference reproducing Spade's truncation
semantics bit-for-bit (0 mismatches).

The spike is intentionally narrower than the fabric: it omits the dyadic
`14/16` decay and the wider accumulator (`ACC_W`), so it is not yet
bit-exact against the golden model. Decision: keep RTL in Verilog and
generation in Python for the PoC; revisit Spade for Stage 2.
