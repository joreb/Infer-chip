# Wiki Index

Content catalog. Every wiki page is listed under its type with a one-line summary. Read this first to find relevant pages for any query.

## References

Reference pages summarize external literature and open-source projects. They are generated from
source indices and rebuilt regularly. Do not hand-edit them. See `SCHEMA.md` for the reason.

Two source indices feed these pages. The nine numbered sections come from the
[Awesome AI for Chips/VLSI/EDA Papers](https://github.com/Archerll/AI4CHIPSpaper) index by Archerll,
which is built on the survey
[*A Survey of Circuit Foundation Model: Foundation AI Models for VLSI Circuit Design and EDA*](https://arxiv.org/pdf/2504.03711)
by the research group of Professor Xie Zhiyao. The `onm-` pages come from the
[Open Neuromorphic resource list](https://github.com/open-neuromorphic/open-neuromorphic). Each page
summary comes from the abstract of the paper on arXiv, written by a local model.

Four limits apply to every reference page:

- The upstream maintainers assign each paper to a section. A paper that covers two tasks appears only
  in the section the source gives it.
- The source index holds preprints and forthcoming work. Some entries carry a date later than the
  date of publication, and this wiki does not correct those dates.
- Some source rows have an empty cell for the name or the venue. Those cells show `n/a`.
- The sub-theme groups and the "Notable entries" text are the editorial layer of this wiki. The
  source indices do not contain them.

Read [Survey and Benchmark](raw/papers/01-survey-and-benchmark.md) first if the field is new to you,
then [RTL](raw/papers/03-rtl.md). To build a design loop, read RTL for the generation step,
[Verification and Debug](raw/papers/04-verification-and-debug.md) for the feedback signal, and
[Flow and Layout](raw/papers/08-flow-and-layout.md) to close on physical measurements.

<!-- generated:references:ai4chips -->
## AI4CHIPS Sections

The index holds 243 papers in 9 sections.

| # | Section | Papers |
|---|---|---|
| 01 | [Survey & Benchmark](raw/papers/01-survey-and-benchmark.md) | 26 |
| 02 | [HLS (High-Level Synthesis)](raw/papers/02-hls.md) | 12 |
| 03 | [RTL (Register Transfer Level)](raw/papers/03-rtl.md) | 97 |
| 04 | [Verification & Debug](raw/papers/04-verification-and-debug.md) | 36 |
| 05 | [Security](raw/papers/05-security.md) | 12 |
| 06 | [Architecture](raw/papers/06-architecture.md) | 15 |
| 07 | [Netlist](raw/papers/07-netlist.md) | 21 |
| 08 | [Flow & Layout](raw/papers/08-flow-and-layout.md) | 14 |
| 09 | [Analog](raw/papers/09-analog.md) | 10 |
<!-- /generated:references:ai4chips -->

<!-- generated:references:neuromorphic -->
## Open Neuromorphic Sections

The index holds 24 entries in 5 sections.

| Section | Entries |
|---|---|
| [onm-snn-training-frameworks-for-ml](raw/papers/onm-snn-training-frameworks-for-ml.md) | 7 |
| [onm-snn-training-frameworks-for-neuroscience](raw/papers/onm-snn-training-frameworks-for-neuroscience.md) | 2 |
| [onm-snn-training-frameworks-for-ml-and-neuroscience](raw/papers/onm-snn-training-frameworks-for-ml-and-neuroscience.md) | 2 |
| [onm-event-based-data-utilities](raw/papers/onm-event-based-data-utilities.md) | 6 |
| [onm-digital-hardware-projects](raw/papers/onm-digital-hardware-projects.md) | 7 |
<!-- /generated:references:neuromorphic -->

## Incidents

Incident pages record defects, limits and decisions in this project with their symptom, root cause, fix and regression test.

- [ENG-001: np.diag on a 2-D matrix returns the 1-D diagonal](incidents/001-np-diag-returns-1d.md). Numpy shape issue in the photonic model diagonal encode step.
- [ENG-002: cocotb results parser lives in check_results and returns a 2-tuple](incidents/002-cocotb-check-results-module.md). Wrong import path and unpacking in the testbench results parser.
- [ENG-003: tail without pipefail hides a make failure](incidents/003-tail-without-pipefail.md). Shell pipeline masks flow failures and reports success for incomplete runs.
- [ENG-004: testbench inject loop over PAD raises IndexError at a non-power-of-two neuron count](incidents/004-tb-range-pad-non-pow2.md). Padding boundary bug in the testbench spike injection loop.
- [ENG-005: make run in the ORFS image is a per-stage noop that returns rc=0](incidents/005-orfs-make-run-is-per-stage-noop.md). Wrong make target in the flow wrapper invokes a noop helper instead of the full PnR.
- [ENG-006: relative docker bind paths are rejected as named volumes](incidents/006-relative-docker-bind-paths.md). Orchestrator-only failure, docker daemon rejects relative paths as volume names before make starts.
- [ENG-007: DESIGN_NAME must equal the generated top module](incidents/007-design-name-equals-top-module.md). Hardcoded config name against a generator-named top module fails yosys elaboration.
- [ENG-009: PnR results never reached the host and metadata.json was never written](incidents/009-copy-out-path-and-no-metadata.md). A cd in the container script broke every copy path, and bare make never writes the metrics file. Beginner tutorial included.
- [ENG-010: parse_metrics took clock-tree-stage values instead of final values](incidents/010-parse-metrics-took-cts-stage-values.md). Metadata holds one key per stage, and the first match was the CTS stage. Beginner tutorial included.

## Bugs

Bug pages record defects with no fix yet, or fixes that span many pages.

- [Concurrent orchestrator invocations clobber one shared run directory](bugs/orchestrator-run-dir-has-no-lock.md). Two runs wrote the same journal and results tree without coordination or error detection. Fixed in a8241a1 with one directory and one `inv` stamp per run. Beginner tutorial included.

## Tutorials

Tutorials teach chip design on this project, for a reader who is new to it. Read them in order.

1. [How the spiking neuron core works](tutorials/how-the-spiking-neuron-core-works.md). LIF neurons in fixed-point, the golden model, the four FSM phases, the weight stores.
2. [From Verilog to a chip layout](tutorials/from-verilog-to-gds.md). RTL, parity simulation, the ORFS stages, where the GDS is, and the pitfalls we found.
3. [How to read the PPA metrics](tutorials/reading-ppa-metrics.md). Power, slack, area, wirelength and DRC; one key per stage; how to compare two runs.
4. [How to run the agent loop](tutorials/running-the-agent-loop.md). Rounds, backends, the run directory, the journal, and how to record evidence.

## Concepts

Concept pages explain an idea or a mechanism.

- [Glossary of key concepts](concepts/glossary.md). 77 terms from accumulator to Yosys, each defined for this project.
- [Weight storage hierarchy, from SSD to the core](concepts/weight-storage-hierarchy.md). Why the core cannot read weights from SSD or DDR5 directly, the load-then-run path (GitHub #11), streaming, and a scale check for 1 T-parameter models. Beginner background included.

## Summaries

Summary pages digest a topic from the literature.

- [Fractal and hierarchical designs for neuromorphic chips](summaries/fractal-and-hierarchical-neuromorphic-designs.md). H-tree, tree and mesh routing in real chips, Rent's rule, and where "fractal" is loose usage. Beginner background included.
- [CMOS compute-in-memory](summaries/cmos-compute-in-memory.md). Digital and analog SRAM CIM, SNN CIM macros, open standard-cell memory tools for sky130, and limits. Beginner background included.

## Comparisons

Comparison pages put two measured designs side by side with a verdict.

- [On-die ROM weights against external SRAM weights, 128 neurons](comparisons/rom-vs-external-sram-weights.md). Dense-ROM baseline (GitHub #2): +5.4% area, +26% wirelength, -2.9% power; the ROM is cheap only because its zero weights are removed.

## Procedures

Procedure pages record how to act in this project.

- [How to add an engineering log entry](procedures/add-an-engineering-log-entry.md). Workflow for documenting bugs, limits and decisions in this log.

## Tasks

Working records grouped by activity rather than by type. This area holds two sub-areas: exploration records and investigation records.

### Musings

Musing pages record dated, immutable decisions and deliberations from a single moment in time.

- [Can one run LLMs on spiking neural network hardware?](tasks/musings/2026-10-17-llms-on-snn-hardware.md). Large-scale spiking language models remain blocked by compute shape and memory bandwidth, not neuron science.
- [BindSNET for model gen and hls4ml for RTL?](tasks/musings/2026-10-17-bindsnet-plus-hls4ml-seam.md). The proposed chain breaks at the seam due to missing SNN support in hls4ml and fundamental architectural mismatch.
- [Why not hls4ml for the fabric itself?](tasks/musings/2026-10-17-why-not-hls4ml-for-the-fabric.md). The block is an event-driven state machine, not a dataflow inference graph; hls4ml adds no hardware value.
- [BindSNET is a trainer, not a golden model](tasks/musings/2026-10-17-bindsnet-not-a-golden-model.md). BindSNET is a PyTorch simulator for learning; it replaces neither the golden model nor a hardware path.
- [SpikeLLM is not a target for the fabric](tasks/musings/2026-10-17-spikellm-is-not-a-target-for-the-fabric.md). SpikeLLM redesigns language models with spiking mechanisms, but the scale and spike mechanism both mismatch our 256-neuron fabric.
- [RISC-V is a control plane for the SNN fabric, not the fabric itself](tasks/musings/2026-10-17-riscv-is-control-plane-not-the-fabric.md). RISC-V alone is not a spiking-LLM engine; RISC-V orchestrating the LIF fabric is, via control-plane or coprocessor patterns, not per-neuron cores.

### Hypotheses

Investigation records for live failures. Each hypothesis stays open while evidence arrives. When the investigation closes, it freezes.

- [Hypothesis set: 1_synth load_design failure (attempt 3)](tasks/hypothesis/2026-10-17-1-synth-load-design-fail.md). Orchestrated 128-neuron PnR run fails at yosys design load with unclear error; full log pending to anchor hypotheses about SDC braces, design binding, memory extraction, or stale artifacts.
