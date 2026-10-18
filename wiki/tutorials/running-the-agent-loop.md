---
title: How to run the agent loop
created: 2026-10-18
updated: 2026-10-18
type: tutorial
tags: [flow, verification, benchmark]
sources: []
---

# Tutorial 4: How to run the agent loop

Text written in ASD-STE100 Simplified Technical English.

**Goal.** After this tutorial, you can run the agent loop, read its journal, and record a run as
evidence that other people can check.

**What you need.** Tutorials [1](how-the-spiking-neuron-core-works.md),
[2](from-verilog-to-gds.md) and [3](reading-ppa-metrics.md).

## 1. What the loop does

The project idea is that an AI agent designs the chip. The agent proposes a configuration, the
tools measure it, and the agent reads the result and proposes the next one. `orchestrator.py` is
this loop. In each **round**:

1. The **backend** (the agent) reads the last 5 journal lines and proposes a config.
2. The loop checks the config. If a key is missing, it uses the previous config, or the default
   config in the first round.
3. If `--seed-config` is given, its keys replace the keys of the config. This happens in every
   round.
4. The **target** evaluates the config: simulation, then flow.
5. If a stage fails, the backend writes an analysis of the failure.
6. The loop adds one line to the **journal**.

## 2. Backends and targets

| Option | Values | Meaning |
|---|---|---|
| `--target` | `digital`, `photonic`, `memristive` | What to design. Only `digital` makes a real layout. The other two use models |
| `--backend` | `stub` (default), `cc`, `api` | `stub` follows a fixed script and proposes nothing by default. `cc` calls Claude Code (`claude -p`). `api` is not available yet |
| `--rounds` | integer, default 5 | Maximum rounds. The loop stops early if the backend proposes nothing |
| `--seed-config` | JSON | Keys that replace the config in every round |
| `--out` | directory, default `runs` | Where the runs and the journal go |

With the `stub` backend and a `--seed-config`, the journal note says "proposed config invalid; fell
back to DEFAULT_CFG". This is expected. The stub proposes nothing, so the loop starts from the
default config, and the seed config then replaces all its keys.

## 3. Run one round

```bash
.venv/bin/python orchestrator.py --target digital --rounds 1 --out runs_tutorial \
  --seed-config '{"neurons": 16, "fanout": 8, "weight_width": 4, "timesteps": 64,
                  "util_target": 25, "clock_ns": 40.0}'
```

A 128-neuron round takes 43 minutes or more. Run long rounds in the background. The flow kills
its container after 7200 s.

## 4. The run directory

```text
runs_tutorial/digital/
  journal.jsonl                  one line per round, all invocations
  round_0/inv_<8 hex>/           one directory per round and per invocation
    orfs/                        the design files given to ORFS
    sim_build/                   the parity simulation
    results/                     results, reports and logs copied from the container
    docker_cmd.txt               the exact docker command
    final.gds                    the layout
```

The **invocation id** (`inv`) is a random 8-character value for each start of the orchestrator.
Two runs at the same time get different directories, and each journal line has its `inv`. Before
this fix, two runs wrote over each other
([run-dir bug](../bugs/orchestrator-run-dir-has-no-lock.md)).

## 5. Read the journal

```bash
tail -1 runs_tutorial/digital/journal.jsonl | .venv/bin/python -m json.tool
```

| Field | Meaning |
|---|---|
| `round`, `inv` | which round of which invocation |
| `config` | the config that was evaluated |
| `sim.verdict` | `pass` if the RTL matches the golden model |
| `sim.bus_bits`, `sim.weight_mbit` | width of the weight port, size of the weight memory |
| `flow.verdict` | `pass`, `fail` or `skipped` |
| `flow.worst_slack_ns`, `pwr_w`, `area_mm2`, `wirelength_um`, `drc` | final PPA values ([tutorial 3](reading-ppa-metrics.md)) |
| `flow.reason` | the error text if the flow failed |
| `agent_note` | the note or failure analysis of the backend |

## 6. Record a run as evidence

A number without a record is not evidence. For each run that you use in a claim:

1. Copy `metadata.json`, `docker_cmd.txt` and the journal line into
   `runs_digital_e2e/digital/evidence/` with a date prefix.
2. Write a short page there: config, commit, image, `inv`, wall time, a table with the metadata
   keys, and the log line for each number.
3. Do not put the GDS in git (it is 8 to 76 MB). Give its path and its sha256.
4. Say what the numbers do not include.

Example: `runs_digital_e2e/digital/evidence/2026-10-18-rom-baseline-pnr-pass.md`.

## Check your understanding

1. You start two orchestrators on the same `--out`. Is this safe? Answer: yes since commit a8241a1.
   Each has its own `inv` directory.
2. The journal says `flow.verdict: skipped`. Why? Answer: the simulation failed, so the flow did
   not start.
3. Why is the `stub` backend useful? Answer: it gives the same result every time, so tests and
   baseline runs do not depend on a model.

## Next

The [glossary](../concepts/glossary.md) lists all terms. For open work, see the GitHub issues and
[weight storage hierarchy](../concepts/weight-storage-hierarchy.md).

Related: [index](../index.md).
