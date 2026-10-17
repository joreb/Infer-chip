---
title: cocotb results parser lives in check_results and returns a 2-tuple
created: 2026-10-17
updated: 2026-10-17
type: incident
tags: [bug, testbench, cocotb, regression-test]
sources: []
---

# ENG-002: cocotb results parser lives in check_results and returns a 2-tuple

Text written in ASD-STE100 Simplified Technical English.

| Field | Value |
|---|---|
| ID | ENG-002 |
| Kind | bug |
| Status | fixed |
| Area | testbench |
| Fix commit | `31e511d` |
| Pinned by | `tests/test_review_fixes.py::test_sim_parity_non_pow2_neurons` |

## Symptom

The first end to end cocotb run raised at the results parse step, after the simulation itself passed:

```python
ImportError: cannot import name 'results' from 'cocotb_tools' (...)
```

## Root cause

`targets/digital/evaluate.py`. Two wrong assumptions at once. One: the results parser lives in
`cocotb_tools.results`. That module does not exist in cocotb 2.x, so the import raises. Two: the parser
returns a tuple, and the old code unpacked it as a single count. The real module is
`cocotb_tools.check_results`, and `get_results(xml) -> (num_tests, num_failed)` returns a 2-tuple.

## Fix

`targets/digital/evaluate.py` lines 61 to 62 import from `cocotb_tools.check_results` and unpack the
2-tuple. Fix commit `31e511d`.

## Regression test

`tests/test_review_fixes.py::test_sim_parity_non_pow2_neurons` runs a real cocotb simulation at 300
neurons and parses the results file the same way the target does. Confirmed against the old code: with
the import reverted to `cocotb_tools.results`, the test fails with `ModuleNotFoundError`; with the
current import it passes.

See also [index](../index.md), [ENG-004](004-tb-range-pad-non-pow2.md), and [procedure](../procedures/add-an-engineering-log-entry.md).
