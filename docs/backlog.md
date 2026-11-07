# Backlog: ideas and possible paths forward

Stage-2 candidate directions for the PoC. Nothing here blocks the SPRIND
pitch (deadline 2026-11-30). Each entry keeps the rejection rationale, so a
future session does not relitigate it.

Discussed 2026-10-17, during the digital e2e PnR run.

## Adopted architecture (baseline, for contrast)

One agentic design loop, three device targets. Config-driven Python
generator (`targets/digital/rtl_gen.py`) emits the parameterized LIF fabric;
numpy golden model is bit-exact against it via cocotb; ORFS docker runs
sky130hs PnR; agent layer proposes configs only, never touches HDL.

Paths below vary what feeds the generator, what languages emit the fabric,
and what blocks share the die.

## 1. Train-and-map: trained SNN weights onto the verified fabric

`snnTorch` (preferred, active) or BindSNET (maintenance mode) trains an SNN
in torch. Then: quantize weights to WW bits, extract the matrix,
`weight_words()` packs it, write as the external SRAM image, run the fabric
and ORFS unchanged.

Why this works with the current architecture: weights are external data by
design (docs/openspike-memory-interface.md), so training changes the SRAM
image, not the netlist.

Value: "a trained SNN running on silicon we placed and routed" is a stronger
jury story than a random-weight fabric.

Deliverable when picked up: quantizer + a cocotb bench that streams
real-data spike trains (Poisson-encoded MNIST) instead of random fanout-8
frames.

## 2. hls4ml for dense ANN blocks (heterogeneous die)

If the demo grows an ANN front-end beside the SNN core (spike encoding,
feature extraction, or an ANN-vs-SNN PPA contrast), generate only the dense
quantized-ANN block with hls4ml (ONNX/Keras in), keep the SNN fabric on the
Python generator, marry both at the ORFS level.

Rejected as the fabric path (kept here with reasons):

- hls4ml ingests inference graphs, not stateful spiking modules; a BindSNET
  network would need a torch-SNN to ONNX exporter that does not exist, and
  hls4ml has no LIF layer to compile the result.
- Its output shape is frame-based dataflow with weights baked in as ROMs,
  which contradicts the peer-accepted external-SRAM OpenSpike port and the
  spike-event streaming cycle budget.
- Three semantics layers (torch floats, HLS fixed point, RTL) would replace
  the single bit-exact numpy-vs-RTL proof; not rebuildable before the pitch.

## 3. Typed HDL for agent-authored modules (Veryl or Spade)

If stage 2 adds agent-authored modules (not just agent-chosen configs) or
multi-core tiling, a typed HDL gives static port/width checking, LSP lint
and package ergonomics. Veryl is a standalone Rust-flavored language that
compiles to plain Verilog (cocotb and ORFS keep working unchanged); Spade
(Rust-based) is the more opinionated "Rust for HDL" option.

Rejected for the PoC: the fabric RTL is small and already parity-verified;
every bug found so far was flow-side (mount paths, make targets, SDC Tcl),
not RTL-side; a language migration adds re-verification debt before the
deadline.

## 4. Demo stimulus upgrade (small, near-term)

Real input data through the existing pipeline: Poisson-encoded digits into
in_spk frames via the cocotb bench, recorded as demo footage next to the
GDS. Independent of entry 1; can use pre-quantized random weights.

## 5. Reference sweep (ledgered, unsurveyed)

reference/EDA_MCP (cloned, git-ignored) was taken in for inspiration and is
still unsurveyed; check it for agent-EDA interface ideas before deciding
stage-2 agent tooling.

## 6. Deferred miner findings (from the ledger)

- rest != 0 LIF decay semantics
- cc-fallback agent_note
- validate_config type checks before api backend
## 7. SDK, API and ecosystem for edge AI (long-term, post-pitch)

A flexible software stack around the fabric: config and weight-packaging APIs,
SPI streaming routines, a reference host trainer, and tooling so edge AI
applications can adopt the core without RTL work. This is the commercial
surface, not the PoC.

Why it is deferred: the PoC must keep the contract minimal (config-driven
generator, external weights by design) so it stays verifiable and tape-out
focused. The SDK should follow the settled interface, not precede it.

When to pick up: after the pitch, once train-and-map and the OpenSpike-style
weight path (docs/openspike-memory-interface.md) are settled.

## 8. LLM inference chip design space (long-term, separate track)

Designing an LLM inference accelerator: a tiled dataflow engine (GEMM arrays,
attention and KV cache, normalization/activation) plus compiler/runtime that
maps a transformer to it, validated end to end against a software model. The
dominant constraints are memory bandwidth, KV cache management and precision,
not ALU throughput. This is out of scope for the current SNN PoC.

Why it is deferred: the PoC targets an edge spiking core; a transformer
accelerator needs HBM/GDDR, a full compiler, and different thermal and I/O
budgets. Starting point for any such work should be a proven open dataflow
accelerator design plus work on memory and compiler.

When to pick up: only as a separate project after the 2026-11-30 pitch.
