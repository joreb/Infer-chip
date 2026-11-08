---
title: Complete wiki decision tree
created: 2026-10-19
updated: 2026-10-19
type: solution
tags: [wiki, decisions, reference, clef]
sources:
  - wiki/index.md
  - wiki/log.md
status: open
---

# Complete wiki decision tree

This page groups wiki pages into areas. A classifier (clef:cloud) labeled each page.
Use it to find a page for a task, fix, or question.

## How to use

Start at the root. Answer one question. Follow the matching branch.

```text
What do you need?
  +-- fix a failure      -> Flow or Verification
  +-- design core RTL     -> Core
  +-- compare options     -> Comparisons
  +-- learn a concept     -> Concepts
  +-- read research       -> Research
  +-- find a task/musing  -> Tasks
  +-- process/meta help   -> Process
```

## Flow and build

- `incidents/003-tail-without-pipefail.md`
- `incidents/005-orfs-make-run-is-per-stage-noop.md`
- `incidents/006-relative-docker-bind-paths.md`
- `incidents/007-design-name-equals-top-module.md`
- `incidents/009-copy-out-path-and-no-metadata.md`
- `incidents/010-parse-metrics-took-cts-stage-values.md`
- `raw/papers/07-netlist.md`
- `raw/papers/08-flow-and-layout.md`
- `tutorials/from-verilog-to-gds.md`
- `tutorials/reading-ppa-metrics.md`

## Verification and simulation

- `incidents/001-np-diag-returns-1d.md`
- `incidents/002-cocotb-check-results-module.md`
- `incidents/004-tb-range-pad-non-pow2.md`

## Core design

- `raw/papers/03-rtl.md`
- `raw/papers/06-architecture.md`
- `summaries/128-neuron-core-performance.md`
- `tutorials/how-the-spiking-neuron-core-works.md`

## Comparisons

- `comparisons/photonic-vs-digital-snn-core.md`
- `comparisons/rom-vs-external-sram-weights.md`

## Concepts and glossary

- `concepts/glossary.md`
- `concepts/weight-storage-hierarchy.md`

## Research and summaries

- `raw/papers/01-survey-and-benchmark.md`
- `raw/papers/02-hls.md`
- `raw/papers/04-verification-and-debug.md`
- `raw/papers/05-security.md`
- `raw/papers/09-analog.md`
- `raw/papers/onm-digital-hardware-projects.md`
- `raw/papers/onm-event-based-data-utilities.md`
- `raw/papers/onm-snn-training-frameworks-for-ml-and-neuroscience.md`
- `raw/papers/onm-snn-training-frameworks-for-ml.md`
- `raw/papers/onm-snn-training-frameworks-for-neuroscience.md`
- `summaries/cmos-compute-in-memory.md`
- `summaries/fractal-and-hierarchical-neuromorphic-designs.md`
- `summaries/on-chip-learning-for-snn-hardware.md`

## Tasks and musings

- `tasks/hypothesis/2026-10-17-1-synth-load-design-fail.md`
- `tasks/hypothesis/2026-10-19-evaluate-fpga-prototype.md`
- `tasks/hypothesis/2026-10-19-spade-spike-for-one-module.md`
- `tasks/musings/2026-10-17-bindsnet-not-a-golden-model.md`
- `tasks/musings/2026-10-17-bindsnet-plus-hls4ml-seam.md`
- `tasks/musings/2026-10-17-llms-on-snn-hardware.md`
- `tasks/musings/2026-10-17-riscv-is-control-plane-not-the-fabric.md`
- `tasks/musings/2026-10-17-spikellm-is-not-a-target-for-the-fabric.md`
- `tasks/musings/2026-10-17-why-not-hls4ml-for-the-fabric.md`
- `tasks/musings/2026-10-18-snn-experience-memory-for-calibration.md`
- `tasks/musings/2026-10-19-edge-robot-integration-spi-not-pcie.md`

## Process and meta

- `SCHEMA.md`
- `bugs/orchestrator-run-dir-has-no-lock.md`
- `index.md`
- `log.md`
- `procedures/add-an-engineering-log-entry.md`
- `tutorials/running-the-agent-loop.md`
