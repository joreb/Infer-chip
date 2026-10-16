# Agentic AI-Native Chip Design — PoC

One agentic design loop, three device targets, journal + Pareto evidence.

| target | sim | flow (PPA) |
|---|---|---|
| `digital` | LIF fabric RTL (Yosys/iverilog, cocotb bit-exact parity vs golden model), weights external via OpenSpike-compatible SRAM port | OpenROAD-flow-scripts docker → sky130hs GDS |
| `photonic` | MZI-mesh transfer-matrix model (numpy) | model PPA: energy/MAC, loss, footprint |
| `memristive` | RRAM crossbar + ADC quantization (numpy) | model PPA: energy/MAC, area, rel error |

## Run

```bash
uv sync
# full-stack, model targets (minutes):
uv run python orchestrator.py --target photonic --backend stub --rounds 3 \
    --seed-config '{"mesh_depth": 4, "precision_bits": 8, "laser_mw": 1.0, "wavelength_nm": 1550}'
uv run python orchestrator.py --target memristive --backend stub --rounds 3 \
    --seed-config '{"xbar_rows": 32, "xbar_cols": 32, "variability_frac": 0.05, "adc_bits": 8}'

# digital, needs iverilog + docker (see targets/digital/flow.py docstring).
# The openroad/orfs image carries the whole flow: no ORFS clone, no ORFS_ROOT.
#   docker pull openroad/orfs:latest
uv run python orchestrator.py --target digital --backend stub --rounds 3 \
    --seed-config "$(cat examples/digital_128.json)"

# agent backend = real Claude Code shellout (`claude -p --model sonnet`):
uv run python orchestrator.py --target photonic --backend cc --rounds 5 --out runs_cc

# Pareto report + PNGs per target:
uv run python -c "from pathlib import Path; from report.pareto import write_report; \
write_report(Path('runs_cc/photonic/journal.jsonl'), Path('runs_cc/report_photonic.md'))"

# tests (dockerless paths included):
uv run pytest
```

Artifacts: `runs/<target>/journal.jsonl` (one record per round: config, sim,
flow, agent_note), `runs*/report_*.md` + `pareto_*.png`.

Demo evidence captured 2026-10-17: digital 128-neuron sim parity PASS ×3
(ORFS PnR in flight), photonic + memristive full pass ×3,
cc backend 5 rounds with distinct configs exploring the design space
(`runs_cc/report_photonic.md`).

Architecture notes: `docs/openspike-memory-interface.md` (external weight
memory port, the fabric holds no weights), `wiki/engineering/` (bugs and
fixes, one page per incident).