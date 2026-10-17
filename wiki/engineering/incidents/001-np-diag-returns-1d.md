---
title: np.diag on a 2-D matrix returns the 1-D diagonal
created: 2026-10-17
updated: 2026-10-17
type: incident
tags: [bug, photonic, numpy, regression-test]
sources: []
---

# ENG-001: np.diag on a 2-D matrix returns the 1-D diagonal

Text written in ASD-STE100 Simplified Technical English.

| Field | Value |
|---|---|
| ID | ENG-001 |
| Kind | bug |
| Status | fixed |
| Area | photonic model |
| Fix commit | `3dd7a68` |
| Pinned by | `tests/test_mesh.py::test_diag_encode_stays_2d` |

## Symptom

The diagonal encode matrix of the MZI mesh comes out with the wrong shape, and numpy does not raise at
the call site. The wrong shape then shows up later, as a shape error or as wrong math downstream:

```python
>>> m = np.eye(4) * 2
>>> np.diag(m).shape
(4,)          # the diagonal vector, not a matrix
>>> np.diagflat(m).shape
(16, 16)      # np.diagflat flattened the 2-D input first
```

## Root cause

`targets/photonic/mesh.py`, the weight encode step. Wrong assumption: one numpy call builds a diagonal
matrix from a matrix. `np.diag` treats a 2-D input as an extract operation and returns a 1-D vector.
`np.diagflat` treats a 2-D input as a flattened vector and returns an n*n matrix of a wrong size.
Neither call keeps the (n, n) shape.

## Fix

`targets/photonic/mesh.py` line 74 uses `np.diagflat(np.diag(M))`: `np.diag` extracts the diagonal and
`np.diagflat` builds the diagonal matrix from the 1-D result. The fix landed inside feature commit
`3dd7a68` before the first version was committed.

## Regression test

`tests/test_mesh.py::test_diag_encode_stays_2d` runs the full mesh and asserts the output keeps the
input shape and stays finite. Not confirmed against the old code: the fix landed before the first
commit, so no commit holds the fault. The repro in the Symptom section is the shape proof.

See also [index](../index.md) and [procedure](../procedures/add-an-engineering-log-entry.md).
