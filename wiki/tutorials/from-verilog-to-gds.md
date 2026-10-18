---
title: From Verilog to a chip layout
created: 2026-10-18
updated: 2026-10-18
type: tutorial
tags: [flow, orfs, docker, verification, layout]
sources: []
---

# Tutorial 2: From Verilog to a chip layout

Text written in ASD-STE100 Simplified Technical English.

**Goal.** After this tutorial, you can make the RTL, test it, and turn it into a GDS layout file
with the project flow. You know what each flow stage does and where its output is.

**What you need.** [Tutorial 1](how-the-spiking-neuron-core-works.md). A Linux shell in the
repository root, with `.venv`, `iverilog` and `docker`. The docker image `openroad/orfs:latest`.

## 1. The path from text to silicon

```text
config (JSON) -> rtl_gen.py -> Verilog -> parity sim (cocotb + iverilog)
              -> ORFS in docker: synthesis -> floorplan -> place -> CTS -> route -> finish
              -> 6_final.gds + metadata.json
```

- **RTL** (Verilog) tells what the logic does.
- **Simulation** runs the RTL in software and checks it against the golden model.
- **Place and route (PnR)** makes the physical layout. We use **OpenROAD-flow-scripts (ORFS)** on
  the **sky130hs** cell library (an open 130 nm process from SkyWater).
- **GDS** is the layout file. A chip factory makes masks from it.

## 2. Run the unit tests

```bash
.venv/bin/python -m pytest -q
```

All tests must pass. The slow test `tests/digital/test_rtb.py` runs the parity simulation.

## 3. Look at the generated Verilog

```bash
.venv/bin/python -c "
from targets.digital.rtl_gen import generate_rtl
print(generate_rtl({'neurons': 16, 'fanout': 8, 'weight_width': 4, 'timesteps': 64,
                    'util_target': 25, 'clock_ns': 40.0}))" | head -40
```

Find the ports `clk`, `in_spk`, `w_read_sram` and `spike_out_addr`. Find the four phases.

## 4. Run a small design through the full flow

A 16-neuron design takes about 8 minutes. A 128-neuron design takes 43 to 103 minutes.

```bash
.venv/bin/python orchestrator.py --target digital --rounds 1 --out runs_smoke16 \
  --seed-config '{"neurons": 16, "fanout": 8, "weight_width": 4, "timesteps": 64,
                  "util_target": 25, "clock_ns": 40.0}'
```

This runs the parity simulation first. If the simulation fails, the flow does not start. Then
`run_pnr()` in `targets/digital/flow.py` starts the ORFS container. [Tutorial 4](running-the-agent-loop.md)
explains the orchestrator.

## 5. What each stage does

The stage logs are in `<run dir>/results/logs/<design>/base/`. The file names start with the stage
number.

| Stage | Log prefix | What it does | Output you can check |
|---|---|---|---|
| Synthesis | `1_` | **Yosys** changes the Verilog into a **netlist** of **standard cells** | cell count, synth area |
| Floorplan | `2_` | Sets the **die** and **core** size from **utilization** (25%), adds power rails | die area |
| Placement | `3_` | Puts each cell at a position. Fixes long nets with buffers | placement density |
| CTS | `4_` | **Clock tree synthesis**: buffers so that the clock gets to each flip-flop at the same time | clock skew |
| Global route | `5_1_` | Plans the wires in a coarse grid | congestion, first real slack (log line `FLW-0009`) |
| Detailed route | `5_2_` | Draws each wire on the metal layers. Repairs **DRC** errors in passes | DRC count, wirelength |
| Finish | `6_` | Adds fill cells, writes `6_final.gds` | final **slack**, **power**, area |

After the flow, `make metadata-generate` writes all numbers into `metadata.json`.

## 6. Find the output

```bash
ls runs_smoke16/digital/round_0/inv_*/
ls runs_smoke16/digital/round_0/inv_*/results/*/base/metadata.json
```

`final.gds` is the layout. `docker_cmd.txt` is the exact docker command. Open the GDS in KLayout to
see the layout.

## Pitfalls that we found

Each pitfall cost us a failed run. Read the incident page before you change the flow.

| Pitfall | Page |
|---|---|
| `make | tail` hides a failure of `make` | [ENG-003](../incidents/003-tail-without-pipefail.md) |
| `make run` in the ORFS image does nothing and returns 0 | [ENG-005](../incidents/005-orfs-make-run-is-per-stage-noop.md) |
| A relative path in `docker -v` is a volume name | [ENG-006](../incidents/006-relative-docker-bind-paths.md) |
| `DESIGN_NAME` must equal the top module name | [ENG-007](../incidents/007-design-name-equals-top-module.md) |
| `cd flow` changed every later path; bare `make` writes no `metadata.json` | [ENG-009](../incidents/009-copy-out-path-and-no-metadata.md) |
| A large ROM stops synthesis at `SYNTH_MEMORY_MAX_BITS` | [ROM comparison](../comparisons/rom-vs-external-sram-weights.md) |

## Check your understanding

1. Why does the flow run the simulation first? Answer: a layout of wrong logic is useless, and PnR
   takes up to two hours.
2. Which stage gives the real wirelength? Answer: detailed route (`5_2_`).
3. Where is the final slack? Answer: `finish__timing__setup__ws` in `metadata.json`.

## Next

[Tutorial 3: How to read the PPA metrics](reading-ppa-metrics.md).

Related: [glossary](../concepts/glossary.md), [index](../index.md).
