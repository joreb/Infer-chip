# Parallel Complex128 Compute Core Design

## Intent

Build a clean-room, compute-only accelerator from public arithmetic requirements. The design is not recovered NVIDIA AD104 silicon and does not reproduce the RTX 4000 Ada layout.

## Goals

- Instantiate 128 independent complex arithmetic lanes.
- Execute the same selected operation in every lane in parallel.
- Support complex addition and complex multiplication.
- Use one signed 64-bit fixed-point real component and one signed 64-bit fixed-point imaginary component per value.
- Reuse `complex128_unit` and the existing OpenROAD-flow-scripts Docker flow.
- Verify all 128 lanes with a self-checking simulation.
- Attempt a full SKY130HS GDSII build without reducing the lane count.

## Interface

Top module: `complex128_gpu_128`.

Inputs: `a_re`, `a_im`, `b_re`, and `b_im`, each 8192 bits wide. Lane `i` uses bits `i*64 +: 64` of each input. Input `op` selects addition when 0 and multiplication when 1.

Outputs: `r_re` and `r_im`, each 8192 bits wide. Lane `i` drives bits `i*64 +: 64` of each output.

The core is combinational. Arithmetic wraps modulo 2^64 at each 64-bit output component, matching the existing unit. No clock, reset, host interface, or memory is added in this version.

## Non-goals

- Shader, graphics, CUDA, ray-tracing, or tensor-core support.
- IEEE floating-point behavior.
- Overflow detection or saturation.
- Per-lane operation selection.
- Binary or microarchitectural compatibility with NVIDIA products.
- A claim that the result is a reverse-engineered AD104 netlist or layout.

## Resource constraint

The prior single unit used 31,852 standard cells and 0.364 mm2 of standard-cell area. Linear scaling predicts about 4.08 million cells and 46.6 mm2 before routing. The host has 7.7 GiB RAM. A full parallel GDSII attempt is required, but completion is not guaranteed. The build must not silently substitute fewer lanes.

## Builder choices

Place the reusable top-level RTL and its self-checking testbench under `spikes/complex128-unit/`. Extend `tools/complex128_to_gds.py` with command-line source, output, and design-name options while retaining its current defaults. Write the new run to `runs_complex128_gpu_gds/`.
