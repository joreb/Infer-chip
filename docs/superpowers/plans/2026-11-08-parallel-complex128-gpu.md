# Parallel Complex128 Compute Core Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build and verify 128 fully parallel complex128 arithmetic lanes, then attempt SKY130HS GDSII generation.

**Architecture:** A combinational Verilog generate loop connects 128 existing `complex128_unit` instances to flattened operand and result buses. The existing Docker-based ORFS wrapper receives the new top-level source and writes a separate run directory.

**Tech Stack:** Verilog, Icarus Verilog, Python standard library, Docker, OpenROAD-flow-scripts, SKY130HS.

**Spec:** `docs/superpowers/specs/2026-11-08-parallel-complex128-gpu-design.md`

## Global Constraints

- Keep exactly 128 parallel lanes for the GDSII attempt.
- Reuse signed 64-bit fixed-point `complex128_unit` arithmetic without changing its behavior.
- Use common `op`: 0 for addition, 1 for multiplication.
- Add no shaders, graphics pipeline, CUDA support, or compatibility claims.
- Do not commit or push unless the user requests it.

## Review Focus

- Lane indexing can connect operands to the wrong result slice; Task 1 checks unique values on all 128 lanes.
- Signed multiplication can differ from unsigned reference math; Task 1 uses signed negative operands and expected values.
- Output truncation can hide width errors; Task 1 includes an overflow case that checks modulo-2^64 behavior.
- A stale GDS can be mistaken for a new result; Task 2 uses a new output directory and verifies that the copied GDS was produced by the current command.
- Full-scale routing can exhaust host resources; Task 2 preserves failure output and never reports success without a fresh `final.gds` and passing metrics.

---

### Task 1: Parallel RTL and Arithmetic Verification

**Files:**
- Create: `spikes/complex128-unit/complex128_gpu_128.v`
- Create: `spikes/complex128-unit/complex128_gpu_128_tb.sv`
- Reuse: `spikes/complex128-unit/complex128_unit.v`

**Interfaces:**
- Produces: `complex128_gpu_128` with 8192-bit `a_re`, `a_im`, `b_re`, `b_im`, `r_re`, and `r_im` ports plus one-bit `op`.
- Consumes: Existing combinational `complex128_unit` for every lane.

- [ ] **Step 1: Write the failing all-lane testbench**

Drive a different small signed complex value into each lane. Check all 128 addition results, then all 128 multiplication results. Include negative operands and one explicit modulo-2^64 overflow case. Print the failing lane and values, and finish with a nonzero error count on any mismatch.

- [ ] **Step 2: Run the test before adding the top module**

Run: `iverilog -g2012 -o /tmp/complex128_gpu_128_tb spikes/complex128-unit/complex128_unit.v spikes/complex128-unit/complex128_gpu_128.v spikes/complex128-unit/complex128_gpu_128_tb.sv && vvp /tmp/complex128_gpu_128_tb`

Expected: FAIL because `complex128_gpu_128.v` does not exist.

- [ ] **Step 3: Implement the minimal generate-loop top module**

Create 128 `complex128_unit` instances. Use indexed part selects `i*64 +: 64` and connect the common `op` to every instance.

- [ ] **Step 4: Run the arithmetic verification**

Run the Step 2 command again.

Expected: compile success, simulation prints `PASS: 128 parallel complex lanes`, and exits with status 0.

### Task 2: Reusable Flow Driver and Full GDSII Attempt

**Files:**
- Modify: `tools/complex128_to_gds.py`
- Create: `runs_complex128_gpu_gds/` through the flow driver

**Interfaces:**
- Consumes: `complex128_gpu_128.v` and `complex128_unit.v` as synthesis sources.
- Produces: `runs_complex128_gpu_gds/run/final.gds` and ORFS metrics when the full flow succeeds.
- Extends the driver with `--src`, `--out`, and `--name`; defaults retain the prior single-unit run.

- [ ] **Step 1: Check the flow driver defaults**

Run: `python tools/complex128_to_gds.py --help`

Expected: help lists source, output, and design-name options without starting Docker.

- [ ] **Step 2: Stage and run the full parallel build**

Run: `python tools/complex128_to_gds.py --src spikes/complex128-unit/complex128_gpu_128.v --out runs_complex128_gpu_gds --name complex128_gpu_128`

The driver must include `complex128_unit.v` in the staged synthesis source and use top module `complex128_gpu_128`.

Expected: a fresh full-flow result. Success requires `final.gds`, passing parsed metrics, and exactly 128 lanes in the staged RTL. Failure requires reporting the decisive ORFS or host-resource error without reducing the design.

- [ ] **Step 3: Verify generated evidence**

Confirm that `runs_complex128_gpu_gds/run/final.gds` exists and is newer than the staged RTL. Parse the new ORFS `metadata.json` with the existing `parse_metrics` function and report standard-cell area, setup slack, DRC count, and file size when available.
