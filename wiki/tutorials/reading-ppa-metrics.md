---
title: How to read the PPA metrics
created: 2026-10-18
updated: 2026-10-18
type: tutorial
tags: [flow, orfs, benchmark]
sources: []
---

# Tutorial 3: How to read the PPA metrics

Text written in ASD-STE100 Simplified Technical English.

**Goal.** After this tutorial, you can read `metadata.json`, find the correct final values, and
compare two runs without errors.

**What you need.** [Tutorial 2](from-verilog-to-gds.md). One finished run, or the real fixture
`tests/digital/fixtures/orfs_real_128/metadata.json` (128 neurons, 2026-10-18).

## 1. PPA: power, performance, area

Chip designers judge a design on three numbers:

| Letter | Metric | Unit | Better is |
|---|---|---|---|
| P | **Power**: energy per second that the chip uses | W or mW | lower |
| P | **Performance**: here, timing **slack** at the target clock | ns | positive |
| A | **Area**: the size of the cells | µm² or mm² | lower |

We also check two more:

- **Wirelength**: the total length of all routed wires. Long wires cost area, delay and power.
- **DRC**: the count of **design rule check** violations. It must be 0, or the factory cannot make
  the chip.

## 2. What slack means

The clock period is 40 ns. A signal leaves a flip-flop, goes through gates and wires, and must get
to the next flip-flop before the next clock edge. **Setup slack** is the time that is left on the
slowest path. **WNS** (worst negative slack) is the slack of the worst path.

- Slack +33 ns: the slowest path needs about 7 ns. The design could run much faster.
- Slack 0 ns: just in time.
- Slack below 0: the chip fails at this clock. Make the clock slower or change the logic.

**Hold slack** checks the opposite: a signal must not arrive too early. It must also be ≥ 0.

## 3. One metric, many stages

The flow measures the design again after each stage. Thus `metadata.json` has one key per stage
for each metric. The stage name is the first part of the key:

```bash
.venv/bin/python -c "
import json
d = json.load(open('tests/digital/fixtures/orfs_real_128/metadata.json'))
for k, v in d.items():
    if 'timing__setup__ws' in k: print(k, v)"
```

| Key | Value (ns) |
|---|---|
| `floorplan__timing__setup__ws` | 35.2907 |
| `cts__timing__setup__ws` | 33.1717 |
| `globalroute__timing__setup__ws` | 32.6825 |
| `finish__timing__setup__ws` | 33.1432 |

**Rule: use the final-stage key.** For each metric, use this key:

| Metric | Key | 128-neuron value |
|---|---|---|
| Setup slack | `finish__timing__setup__ws` | +33.1432 ns |
| Power | `finish__power__total` | 0.0141645 W |
| Area | `finish__design__instance__area__stdcell` | 704,933 µm² |
| Wirelength | `detailedroute__route__wirelength` | 1,449,559 µm |
| DRC | `detailedroute__route__drc_errors` | 0 |

Wirelength before detailed routing is only an estimate. The CTS-stage estimate here is 1,282,660
µm, 11.5% too low. A parser that took the first key gave this wrong value to the agent
([ENG-010](../incidents/010-parse-metrics-took-cts-stage-values.md)). `parse_metrics()` in
`targets/digital/flow.py` now reads the keys in the table above.

```bash
.venv/bin/python -c "
from pathlib import Path
from targets.digital.flow import parse_metrics
print(parse_metrics(Path('tests/digital/fixtures/orfs_real_128')))"
```

## 4. Area: which area?

There are three area numbers. Do not mix them.

| Number | Key | 128-neuron value | Meaning |
|---|---|---|---|
| Cell area | `finish__design__instance__area__stdcell` | 0.705 mm² | logic cells only. This is what we compare |
| Core area | `finish__design__core__area` | 2.53 mm² | the area where cells can go |
| Die area | `finish__design__die__area` | 2.54 mm² | the full chip |

**Utilization** = cell area / core area, here about 28%. The flow sets the core from the
utilization target, so a design with more cells also gets a larger die.

## 5. How to compare two runs

1. Use the same config, except the one thing that you test.
2. Use the same keys for both runs. Do not compare a log-line value from one run with a metadata
   value from another run.
3. Give the ratio (new / old) for each metric. A chart with the old run at 1.0 shows all metrics on
   one axis.
4. Say what the numbers do not include. Example: the external-SRAM design area does not include
   its SRAM ([ROM comparison](../comparisons/rom-vs-external-sram-weights.md)).
5. Run the same config twice if you can. Our two 128-neuron external runs gave identical area,
   wirelength and slack. Thus the flow is deterministic for one config and one image.

## Check your understanding

1. Slack is +2 ns at 40 ns. Can the clock go to 30 ns? Answer: probably not. The slowest path
   needs about 38 ns, which is more than 30 ns.
2. Why is the global-route slack not the final slack? Answer: detailed routing and finish change
   the wires and the cells after global route.
3. A design has DRC = 3. Is it done? Answer: no. The factory cannot make it.

## Next

[Tutorial 4: How to run the agent loop](running-the-agent-loop.md).

Related: [glossary](../concepts/glossary.md), [index](../index.md).
