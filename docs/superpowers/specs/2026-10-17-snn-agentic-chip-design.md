# Agentic SNN-Chip Design Loop — SPRIND PoC

**Date:** 2026-10-17
**Status:** Approved
**Purpose:** Proof-of-concept demonstrator for the SPRIND × NADI "AI-Native Chip Design" challenge (deadline 2026-11-30, 11:00 CET). Shows an autonomous agent loop designing a neuromorphic spiking-neural-network core from architecture search through GDSII, using the open OpenROAD flow.

## Goals

- End-to-end unattended loop: **agent proposes config → RTL generated → simulation gated → OpenROAD synthesis/PnR → GDS + metrics → agent learns → next round**
- Produce proposal-grade artifacts: run journal, PPA Pareto front, GDS render, loop architecture diagram
- Ship a minimal working slice first (256 neurons), scale via one config dict (config-driven to ~1k neurons on this 8-core / 8 GB machine)

## Non-Goals

- Agents writing RTL from scratch each round (stage-1 upgrade path, same interfaces)
- Analog/memristive/MoS2 implementations — digital LIF only for the PoC
- Post-signoff (DRC-clean at leading edge is out of scope; sky130 open PDK evidence is sufficient)
- Fabrication or FPGA tape-out

## Architecture

```
        ┌──────────── orchestrator (CLI, round loop) ────────────┐
        │                                                        │
        ▼                                                        ▼
  [arch agent] ──► config.json ──► [rtl gen] ──► core.v ──► [sim: cocotb+iverilog]
        ▲                                                        │ pass?
        │                                                        ▼ fail
        │  metrics.json (area, power, slack, DRC, wirelength)   retry w/ agent fix note (≤2)
        │                                                        ▼
        └──────────── [PPA reporter] ◄── [ORFS docker: syn→PnR→GDS, sky130]
```

The orchestrator owns the loop; agents are swappable strategy providers behind a config flag.

### Agent layer

- `AGENTS_BACKEND=cc` — **current demo mode.** Claude Code agents drive architecture search and failure analysis. Orchestrator emits task prompts + journal path; no LLM API dependency.
- `AGENTS_BACKEND=api` — LLM router: a task classifier selects which model (cheap for log parsing/summarizing, strong for architecture decisions) handles each task. Model roster in config. Behind flag, built after the cc demo works.
- `AGENTS_BACKEND=stub` — deterministic scripted config list. Full pipeline runs agentless; used for tests and CI.

Backend contract (`agents/base.py`):

```python
class Backend:
    def propose_config(self, journal) -> Config: ...
    def analyze_failure(self, stage: str, logs: str, config: Config) -> FixNote: ...
```

## Components

| Component | Job | Tech |
|---|---|---|
| `snn_core/rtl_gen.py` | Config dict → Verilog: parameterized LIF neuron array, synapse crossbar, spike inject/read ports | Plain Python string templating |
| `snn_core/model.py` | Golden numpy LIF reference model | numpy only |
| `sim/` | Cocotb testbench: spike-train parity vs golden model, latency/throughput checks | cocotb + iverilog |
| `flow/orfs.py` | Wraps OpenROAD-flow-scripts docker: mounts design, patches config.mk, runs synth→PnR→GDS on sky130, parses metrics (area, power, worst slack, DRC count, wirelength) | Python + docker CLI |
| `agents/` | Backend interface + cc / api-router / stub implementations | Python |
| `orchestrator.py` | Round loop, bounded retries, budget, journal | CLI |
| `runs/<round>/` | Per-round Verilog, logs, metrics.json | — |

Config surface: `neurons`, `fanout`, `weight_width`, `timesteps`, `util_target`, `clock_ns`. The 256-neuron smoke config ships with the repo.

## Data Flow

`journal.jsonl` is the spine. Each round appends one record:

```json
{"round": 4, "config": {...}, "sim": {"verdict": "pass", "max_err": 0}, "pnr": {"verdict": "pass",
 "area": 0.031, "power_w": 0.042, "worst_slack": 0.11, "drc": 0}, "agent_note": "..."}
```

The Pareto front (silicon area vs energy-per-spike) is derived from the journal. Failures never block the loop: a stage failure is a bounded retry (≤2, with agent fix note), then the round is skipped with the reason recorded.

## Error Handling

- Stub backend lets the whole pipeline run without any LLM
- ORFS docker run gets a timeout + one retry
- Config gate warns when a config likely exceeds the 8 GB WSL memory ceiling
- Stage failures become verdict objects in the journal — data, not exceptions

## Testing

1. Golden-model unit test — fixed seeds, known spike patterns
2. RTL parity test — cocotb sim matches golden model on random spike trains
3. ORFS wrapper test — run one ORFS bundled example design, assert metrics parse
4. Orchestrator smoke — stub agents, 2 rounds, tiny config; assert journal + Pareto report produced

## Deliverables (before 2026-11-30)

1. Unattended multi-round run log (journal.jsonl with ≥5 rounds)
2. PPA Pareto front chart (area vs energy-per-spike)
3. One GDS render of the best config
4. One-page loop architecture diagram
5. This spec + implementation plan, referenced in the SPRIND application as feasibility evidence

## Environment

- WSL2, 8 cores, 8 GB RAM, 58 GB disk free
- Docker 28.5.2 present; OpenROAD-flow-scripts via docker (first build downloads multi-GB PDK)
- No EDA tools on host; iverilog + cocotb installed into a uv venv
- sky130 open PDK, no NDA artifacts

## Risks

| Risk | Mitigation |
|---|---|
| 8 GB RAM ceiling in PnR | Config gate; 256-neuron smoke config closes comfortably |
| Agents emit bad configs | Sim gate before any synthesis spend; bounded retries |
| ORFS docker bandwidth | One-time multi-GB pull, cached thereafter |
| LLM API cost (api backend) | Stub + cc backends carry the whole demo; api router optional |