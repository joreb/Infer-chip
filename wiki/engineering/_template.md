# ENG-NNN: short title in plain words

Text written in ASD-STE100 Simplified Technical English.

| Field | Value |
|---|---|
| ID | ENG-NNN |
| Kind | bug, or decision, or limit |
| Status | open, or fixed, or accepted |
| Area | golden model, or RTL, or testbench, or flow |
| Fix commit | `<sha>` or n/a |
| Pinned by | `path/to/test.py::test_name` or n/a |

## Symptom

What a person sees when the fault happens. Give the exact error text in a code block. Give the command
that produces it. Do not explain the cause here.

```
paste the shortest decisive line of output
```

## Root cause

Why the fault happens. Name the file and the line. State the wrong assumption in one sentence. If the
fault was visible only under one condition, name that condition, for example a non-power-of-two neuron
count.

## Fix

What changed, and where. Keep this short, because the commit holds the detail.

## Regression test

The test that fails if the fault returns. Name the file and the test function. State what the test
asserts. The test must fail on the old code. If nobody confirmed that, write "not confirmed against the
old code" here, because an unproven regression test is not a regression test.

## Notes

Anything a future reader needs. Delete this section if it is empty.

---
[Engineering log index](README.md)
