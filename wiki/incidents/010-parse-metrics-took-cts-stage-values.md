---
title: parse_metrics took clock-tree-stage values instead of final values
created: 2026-10-18
updated: 2026-10-18
type: incident
tags: [bug, flow, orfs, regression-test]
sources: []
---

# ENG-010: parse_metrics took clock-tree-stage values instead of final values

Text written in ASD-STE100 Simplified Technical English.

| Field | Value |
|---|---|
| ID | ENG-010 |
| Kind | bug |
| Status | fixed |
| Area | flow (`targets/digital/flow.py`, `parse_metrics`) |
| Fix commit | `f6d6b51` |
| Pinned by | `tests/digital/test_flow_parse.py::test_parse_metrics_picks_final_stage_values_from_real_metadata` |

## Background for beginners

Read this section if you are new to chip design.

The PnR flow has stages: synthesis, floorplan, placement, clock tree synthesis (CTS), global
route, detailed route and finish. [ENG-009](009-copy-out-path-and-no-metadata.md) explains each
stage. The tool measures the design again after each stage. Each measurement is better than the
one before it, because each stage knows more about the real chip:

- Before routing, the wirelength is an **estimate**. The real wires do not exist yet.
- After detailed routing, the wirelength is the **real** length of the drawn wires.
- The timing slack changes after each stage, because each stage adds or moves cells and wires.

**What slack means.** The clock period is 40 ns. A signal must get from one flip-flop to the next
in less than 40 ns. Slack is the time that is left over. Positive slack is good. Negative slack
means that the chip does not work at this clock speed.

ORFS writes all stages into one `metadata.json` file. Each metric has one key for each stage. The
stage name is the start of the key:

| Key | Value | Stage |
|---|---|---|
| `cts__timing__setup__ws` | 33.1717 ns | after CTS |
| `globalroute__timing__setup__ws` | 32.6825 ns | after global route |
| `finish__timing__setup__ws` | 33.1432 ns | final |

The keys are in alphabetical order. Thus `cts__` comes before `finish__`.

The number that tells you about the real chip is the final number. For wirelength, it is the
detailed-route number.

## Symptom

The orchestrated run of 2026-10-18 passed. The journal line gave these values to the agent:

```text
"worst_slack_ns": 33.1717, "pwr_w": 0.0142308, "area_mm2": 0.704749, "wirelength_um": 1282660.0
```

The stage log gave a routed wirelength of 1,449,559 um. The journal value was 11.5% lower. All
four values were the CTS-stage values.

## Root cause

`parse_metrics` used `_pick_num`, which returns the first key that contains a pattern. The old
patterns did not name a stage:

```python
slack = first(("timing__setup__ws", "percent"), ("__setup__ws", "percent"))
pwr = first(("power__total", None))
area = first(("instance__area__stdcell", None), ("instance__area", None))
wl = first(("wirelength__estimated", None), ("wirelength", "__min"))
```

`cts__timing__setup__ws` is the first key that contains `timing__setup__ws`. The same is true
for power, area and wirelength. The wirelength pattern also asked for the estimate, not for the
routed value.

The wrong assumption: "each metric has one key in `metadata.json`." The old test fixture had one
key for each metric, so the test did not see the fault. The fault was visible only on real
metadata. Real metadata did not get to the host before ENG-009 was fixed.

The DRC value was correct, but only by chance. The first key that contains `drc_errors` is
`detailedroute__route__drc_errors` (0). The next key is `..._iter__0` (530), the count after the
first router pass.

## Fix

`f6d6b51` names the final-stage key first for each metric. The old patterns stay as fallbacks
for old or renamed keys:

```python
slack = first(("finish__timing__setup__ws", "percent"),
              ("timing__setup__ws", "percent"), ("__setup__ws", "percent"))
pwr = first(("finish__power__total", None), ("power__total", None))
drc = first(("detailedroute__route__drc_errors", "iter"),
            ("drc_errors", "iter"), ("design__violations", None))
area = first(("finish__design__instance__area__stdcell", None),
             ("instance__area__stdcell", None), ("instance__area", None))
wl = first(("detailedroute__route__wirelength", "iter"),
           ("wirelength__estimated", None), ("wirelength", "__min"))
```

The DRC pick now excludes the per-pass `iter` keys on purpose. It does not depend on key order.

## Regression test

`test_parse_metrics_picks_final_stage_values_from_real_metadata` reads
`tests/digital/fixtures/orfs_real_128/metadata.json`. This file is the real metadata of the
2026-10-18 run. The test asserts these values:

| Metric | Value | Key |
|---|---|---|
| Slack | 33.1432 ns | `finish__timing__setup__ws` |
| Power | 0.0141645 W | `finish__power__total` |
| Area | 0.704933 mm² | `finish__design__instance__area__stdcell` |
| Wirelength | 1,449,559 um | `detailedroute__route__wirelength` |
| DRC | 0 | `detailedroute__route__drc_errors` |

CONFIRMED: the test fails on the old code and passes after the fix.

## Notes

**Second effect: a wrong label in the evidence.** The run of 2026-10-17 reported a slack of
+32.682 ns from the log line `FLW-0009`. ORFS prints that line at the global-route stage. The
final slack is +33.1432 ns. Both values are positive, so the timing verdict does not change. The
evidence page of 2026-10-17 now has the correct label.

**Lesson for beginners.** When a tool gives one metric many times, find out which number is the
final one before you use it. Make test fixtures from real tool output, not from a short copy that
you wrote by hand.

Related: [ENG-009](009-copy-out-path-and-no-metadata.md),
[ENG-005: make run is a per-stage noop](005-orfs-make-run-is-per-stage-noop.md),
[index](../index.md), [procedure](../procedures/add-an-engineering-log-entry.md).
