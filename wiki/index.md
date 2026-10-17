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

Read [Survey and Benchmark](references/01-survey-and-benchmark.md) first if the field is new to you,
then [RTL](references/03-rtl.md). To build a design loop, read RTL for the generation step,
[Verification and Debug](references/04-verification-and-debug.md) for the feedback signal, and
[Flow and Layout](references/08-flow-and-layout.md) to close on physical measurements.

<!-- generated:references:ai4chips -->
## AI4CHIPS Sections

The index holds 243 papers in 9 sections.

| # | Section | Papers |
|---|---|---|
| 01 | [Survey & Benchmark](references/01-survey-and-benchmark.md) | 26 |
| 02 | [HLS (High-Level Synthesis)](references/02-hls.md) | 12 |
| 03 | [RTL (Register Transfer Level)](references/03-rtl.md) | 97 |
| 04 | [Verification & Debug](references/04-verification-and-debug.md) | 36 |
| 05 | [Security](references/05-security.md) | 12 |
| 06 | [Architecture](references/06-architecture.md) | 15 |
| 07 | [Netlist](references/07-netlist.md) | 21 |
| 08 | [Flow & Layout](references/08-flow-and-layout.md) | 14 |
| 09 | [Analog](references/09-analog.md) | 10 |
<!-- /generated:references:ai4chips -->

<!-- generated:references:neuromorphic -->
## Open Neuromorphic Sections

The index holds 24 entries in 5 sections.

| Section | Entries |
|---|---|
| [onm-snn-training-frameworks-for-ml](references/onm-snn-training-frameworks-for-ml.md) | 7 |
| [onm-snn-training-frameworks-for-neuroscience](references/onm-snn-training-frameworks-for-neuroscience.md) | 2 |
| [onm-snn-training-frameworks-for-ml-and-neuroscience](references/onm-snn-training-frameworks-for-ml-and-neuroscience.md) | 2 |
| [onm-event-based-data-utilities](references/onm-event-based-data-utilities.md) | 6 |
| [onm-digital-hardware-projects](references/onm-digital-hardware-projects.md) | 7 |
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

## Procedures

Procedure pages record how to act in this project.

- [How to add an engineering log entry](procedures/add-an-engineering-log-entry.md). Workflow for documenting bugs, limits and decisions in this log.
