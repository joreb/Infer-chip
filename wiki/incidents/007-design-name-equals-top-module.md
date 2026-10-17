---
title: DESIGN_NAME must equal the generated top module
created: 2026-10-17
updated: 2026-10-17
type: incident
tags: [bug, flow, orfs, yosys, regression-test]
sources: []
---

# ENG-007: DESIGN_NAME must equal the generated top module

Text written in ASD-STE100 Simplified Technical English.

| Field | Value |
|---|---|
| ID | ENG-007 |
| Kind | bug |
| Status | fixed |
| Area | flow (targets/digital/flow.py, write_design config.mk) |
| Fix commit | `0090dc2` |
| Pinned by | `tests/digital/test_flow_parse.py::test_write_design_creates_config_and_rtl` |

## Symptom

The first PnR attempt with the real orchestrator reached yosys and died at the
canonicalize step, under one second of yosys work. The journal held the verbatim error
from the yosys stage:

```text
ERROR: Module `snn_core' not found!
ERROR: TCL interpreter returned an error: Yosys command produced an error
make[1]: *** [Makefile:305: do-yosys-canonicalize] Error 1
```

Docker was healthy, the mounts worked, the file was in place. Only the name was wrong.

## Root cause

`write_design` hardcoded `export DESIGN_NAME = snn_core` in config.mk, but the generated
RTL declares its top as `snn_core_<neurons>`, produced by `module_name(cfg)` in
`targets/digital/rtl_gen.py`. The top module name is a function of the generator, not a
constant somebody can type: change the neuron count in the config and the module name
changes with it. Yosys elaborated with `DESIGN_NAME` as its hierarchy top and found no
such module.

The `write_design` comment even said "must equal top module exactly" while the code
wrote a constant below it. The comment described the constraint the code violated.

## Fix

`DESIGN_NAME` and `DESIGN_NICKNAME` both come from `module_name(cfg)`:

```python
f"export DESIGN_NAME = {name}\n"
f"export DESIGN_NICKNAME = {name}\n"  # names the results dir
```

The nickname stays, to keep naming the results dir, and now stays equal to it.

## Regression test

`tests/digital/test_flow_parse.py::test_write_design_creates_config_and_rtl` asserts
`DESIGN_NAME = snn_core_256` in the generated config for a 256-neuron config. CONFIRMED:
the assertion fails on the pre-fix code, which wrote `DESIGN_NAME = snn_core`.

## Notes

This fault class returns whenever the generator naming changes, which the non-power-of-two
work in [ENG-004](004-tb-range-pad-non-pow2.md) made more likely. The pin is cheap because
`make run` of a broken config dies in under a second, but a missing pin means the failure
reappears at the first config change. Related: [ENG-006](006-relative-docker-bind-paths.md),
which this run also met. See also [index](../index.md) and
[procedure](../procedures/add-an-engineering-log-entry.md).
