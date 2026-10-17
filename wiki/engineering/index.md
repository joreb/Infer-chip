# Wiki Index

> Content catalog. Every wiki page listed under its type with a one-line summary.
> Read this first to find relevant pages for any query.
> Last updated: 2026-10-17 | Total pages: 8

## Incidents

- [ENG-001: np.diag on a 2-D matrix returns the 1-D diagonal](incidents/001-np-diag-returns-1d.md). Numpy shape issue in the photonic model diagonal encode step
- [ENG-002: cocotb results parser lives in check_results and returns a 2-tuple](incidents/002-cocotb-check-results-module.md). Wrong import path and unpacking in the testbench results parser
- [ENG-003: tail without pipefail hides a make failure](incidents/003-tail-without-pipefail.md). Shell pipeline masks flow failures and reports success for incomplete runs
- [ENG-004: testbench inject loop over PAD raises IndexError at a non-power-of-two neuron count](incidents/004-tb-range-pad-non-pow2.md). Padding boundary bug in the testbench spike injection loop
- [ENG-005: make run in the ORFS image is a per-stage noop that returns rc=0](incidents/005-orfs-make-run-is-per-stage-noop.md). Wrong make target in the flow wrapper invokes a noop helper instead of the full PnR
- [ENG-006: relative docker bind paths are rejected as named volumes](incidents/006-relative-docker-bind-paths.md). Orchestrator-only failure, docker daemon rejects relative paths as volume names before make starts
- [ENG-007: DESIGN_NAME must equal the generated top module](incidents/007-design-name-equals-top-module.md). Hardcoded config name against a generator-named top module fails yosys elaboration

## Procedures

- [How to add an engineering log entry](procedures/add-an-engineering-log-entry.md). Workflow for documenting bugs, limits, and decisions in this log
