# Spade spike for one LIF update

Scoped, additive experiment referenced by issue #16 and the Typed HDL
backlog item. It does **not** replace the Python generator or the cocotb
bench.

- Source: `src/main.spade`
- Build: `swim build`
- Synthesis check: `swim synth`

The module compiles and synthesizes to 42 `SB_LUT4` + 15 `SB_CARRY` on
the iCE40 flow. The main friction is Spade's exact-width arithmetic:
each `+` / `-` needs an explicit `trunc::<...>` rather than automatic
widening.
