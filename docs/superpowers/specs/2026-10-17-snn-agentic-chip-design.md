# Agentic SNN-Chip Design Loop — SPRIND PoC

**Date:** 2026-10-17
**Status:** Approved (rev 2 — multi-target)
**Purpose:** Proof-of-concept demonstrator for the SPRIND × NADI "AI-Native Chip Design" challenge (deadline 2026-11-30, 11:00 CET). Shows one autonomous agent loop designing AI-inference chips from architecture search through layout, across three device targets: **digital CMOS (OpenROAD), photonic (inference meshes), memristive (in-memory crossbar)** — using open tooling throughout.

## Goals

- One design loop, many targets: **agent proposes config → device-circuit model generated → simulation gated → flow backend → PPA metrics → agent learns → next round**
- Digital target closes end-to-end to GDSII via OpenROAD (sky130): the headline evidence
- Photonic and memristive targets demonstrate the same loop on physical device models with energy/latency PPA — cross-paradigm breadth is the differentiation
- Produce proposal-grade artifacts: run journal, per-target PPA Pareto fronts, GDS render, loop architecture diagram
- Minimal working slice first: 256-neuron digital config; every target scales via one config dict

## Non-Goals

- Agents writing RTL/layout from scratch each round (stage-1 upgrade path, same interfaces)
- Fabrication or tape-out
- EM-level photonic simulation (Meep) in the PoC — transfer-matrix circuit models suffice; Meep/SAX/gdsfactory integration is stage-1
- Post-signoff (DRC-clean at leading edge out of scope; sky130 open-PDK evidence sufficient)

## Architecture

```
        ┌────────────────── orchestrator (CLI, round loop) ──────────────────┐
        │ target: digital | photonic | memristive   (per target: model+flow) │
        ▼                                                                    ▼
  [arch agent] ──► config.json ──► [target backend] ──► netlist/artifact ──► [sim gate]
        ▲                                                                    │ pass?
        │                                                                    ▼ fail
        │   metrics.json (area, power, latency, energy/op)                   retry w/ fix note (≤2)
        │                                                                    ▼
        └────────────── [PPA reporter] ◄────────────────────── [flow backend]
```

### Targets

| Target | Device model (golden sim) | Flow backend | PoC depth |
|---|---|---|---|
| `digital` | Parameterized LIF fabric, numpy reference | OpenROAD-flow-scripts docker, sky130, GDS + DRC count | **Full: GDS by Nov 30** |
| `photonic` | MZI-mesh tensor core, transfer-matrix sim (numpy/torch), energy-per-MAC model | Layout backend stubbed (gdsfactory in stage 1) | Loop + PPA: energy-per-MAC, insertion loss, footprint |
| `memristive` | RRAM crossbar: conductance-cell model with device variability (numpy), ADC/DAC quantization | Layout backend stubbed (stage 1) | Loop + PPA: energy-per-MAC, area model, accuracy-vs-variability sweep |

Target contract (`targets/base.py`): each target implements `build(config) -> Artifact`, `simulate(artifact) -> SimVerdict`, `run_flow(artifact) -> Metrics`, shared by orchestrator. Agent layer is target-agnostic.

### Agent layer (target-agnostic, swappable)

- `AGENTS_BACKEND=cc` — **current demo mode.** Claude Code agents drive architecture search and failure analysis across all three targets. No LLM API dependency.
- `AGENTS_BACKEND=api` — LLM router: task classifier selects cheap model (log parsing) or strong model (architecture decisions) per task. Roster in config. Behind flag, built after cc demo works.
- `AGENTS_BACKEND=stub` — deterministic scripted config lists per target. Pipeline runs agentless; used for tests.

Backend contract (`agents/base.py`):

```python
class Backend:
    def propose_config(self, journal, target: str) -> Config: ...
    def analyze_failure(self, stage: str, logs: str, config: Config) -> FixNote: ...
```

## Components

| Component | Job | Tech |
|---|---|---|
| `targets/digital/rtl_gen.py` | Config dict → Verilog: LIF neuron array, synapse crossbar, spike inject/read ports | Python string templating |
| `targets/digital/model.py` | Golden numpy LIF reference | numpy |
| `targets/digital/flow.py` | ORFS docker wrapper: synth→PnR→GDS on sky130, parse area/power/slack/DRC | Python + docker CLI |
| `targets/photonic/mesh.py` | MZI-mesh transfer-matrix model, energy-per-MAC PPA | numpy/torch |
| `targets/memristive/crossbar.py` | RRAM crossbar model, variability + ADC/DAC quantization, energy/area PPA | numpy |
| `sim/` | Cocotb testbench (digital): spike-train parity vs golden, latency/throughput | cocotb + iverilog |
| `agents/` | Backend interface + cc / api-router / stub | Python |
| `orchestrator.py` | Round loop per target, bounded retries, budget, journal | CLI |
| `runs/<target>/<round>/` | Per-round artifacts, logs, metrics.json | — |

## Data Flow

`journal.jsonl` is the spine. Each round appends one record:

```json
{"round": 4, "target": "memristive", "config": {...},
 "sim": {"verdict": "pass", "max_err": 0.003},
 "flow": {"verdict": "pass", "area_mm2": 0.031, "pwr_w": 0.042,
         "energy_per_mac_pj": 0.9, "drc": 0},
 "agent_note": "..."}
```

Pareto fronts derived per target from the journal (area vs energy-per-op; photonic: footprint vs energy-per-MAC; memristive: accuracy-loss vs energy-per-MAC). Failures never block the loop: bounded retry (≤2, with agent fix note), then round skipped with reason.

## Error Handling

- Stub backend runs pipeline with no LLM
- ORFS docker timeout + one retry
- Config gate warns when digital config likely exceeds 8 GB WSL memory
- Stage failures become verdict objects — data, not exceptions

## Testing

1. Golden-model unit tests per target — fixed seeds, known stimulus/response
2. RTL parity test — cocotb sim matches golden LIF model on random spike trains
3. ORFS wrapper test — run one ORFS bundled example, assert metrics parse
4. Orchestrator smoke — stub agents, 2 rounds, tiny config per target; assert journal + Pareto reports

## Deliverables (before 2026-11-30)

1. Unattended multi-round run log (journal.jsonl, ≥5 rounds per target)
2. PPA Pareto fronts — digital to GDS; photonic + memristive on device models
3. GDS render of best digital config
4. One-page loop architecture diagram (one loop, three targets)
5. Stage-1 roadmap: RTL-from-scratch agents, gdsfactory/Meep/SAX photonic layout closure, memristive array layout

## Environment

- WSL2, 8 cores, 8 GB RAM, 58 GB disk free
- Docker 28.5.2 present; ORFS via docker (first build downloads multi-GB PDK)
- No EDA tools on host; iverilog + cocotb in a uv venv
- sky130 open PDK, no NDA artifacts
- Photonic reference material: Sacher/ALPS, Fraunhofer HHI PIC deck, existing Meep scripts and ring-resonator GDS in SPRIND research folder

## Risks

| Risk | Mitigation |
|---|---|
| 8 GB RAM ceiling in PnR | Config gate; 256-neuron smoke config closes comfortably |
| Three-target breadth eats calendar | Digital is the only GDS commitment; other two are model-level (numpy) — deliberately cheap |
| Agents emit bad configs | Sim gate before synthesis spend; bounded retries |
| ORFS docker bandwidth | One-time multi-GB pull, cached thereafter |
| LLM API cost (api backend) | Stub + cc backends carry the demo; api router optional |