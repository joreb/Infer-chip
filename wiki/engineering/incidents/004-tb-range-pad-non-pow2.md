---
title: testbench inject loop over PAD raises IndexError at a non-power-of-two neuron count
created: 2026-10-17
updated: 2026-10-17
type: incident
tags: [bug, testbench, cocotb, regression-test]
sources: []
---

# ENG-004: testbench inject loop over PAD raises IndexError at a non-power-of-two neuron count

Text written in ASD-STE100 Simplified Technical English.

| Field | Value |
|---|---|
| ID | ENG-004 |
| Kind | bug |
| Status | fixed |
| Area | testbench |
| Fix commit | `b4b2e0a` |
| Pinned by | `tests/test_memory_interface.py::test_weight_words_pad_sources_are_zero` |

## Symptom

The cocotb parity simulation passes at power-of-two neuron counts and dies at any other count. With
300 neurons, PAD is 512, and the inject loop walks sources 0 to 511:

```python
IndexError: index 300 is out of bounds for axis 1 with size 300
```

## Root cause

`tests/digital/tb_parity.py`, the inject loop. Wrong assumption: the source count equals the padded
array size. The fabric pads 300 neurons to PAD=512, but the spike train has only 300 real columns, so
`frame[s]` raises at s=300. Padding rows sit idle and must hold no inject at all.

## Fix

`tests/digital/tb_parity.py` loops sources with `for s in range(n)`. Padding sources inject nothing.
Fix commit `b4b2e0a`.

## Regression test

`tests/test_review_fixes.py::test_sim_parity_non_pow2_neurons` runs a real cocotb parity simulation at
300 neurons and asserts zero failed cocotb tests. Confirmed against the old code during the review fix
pass: the inject loop boundary was reverted to `range(pad)` and the test failed with the IndexError
above, then passed again after the revert.

## Notes

The external memory interface of commit `a78a6b7` removed the per-source inject loop from the
testbench, so this fault cannot come back in the same shape. The original pin,
`tests/test_review_fixes.py::test_sim_parity_non_pow2_neurons`, is historical: its guarded code no
longer exists, so it cannot fail for the documented reason. The forward pin is the zero words for pad
sources. The fault class, padding counted as data, now lives at the weight memory words, and any future
protocol change reintroduces it there unless the pad words stay zero.

See also [index](../index.md), [ENG-002](002-cocotb-check-results-module.md), and [procedure](../procedures/add-an-engineering-log-entry.md).
