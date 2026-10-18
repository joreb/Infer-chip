---
title: Concurrent orchestrator invocations clobber one shared run directory
created: 2026-10-17
updated: 2026-10-18
type: bug
tags: [flow, testbench, regression-test]
sources: []
status: closed
---

# Concurrent orchestrator invocations clobber one shared run directory

Text written in ASD-STE100 Simplified Technical English.

**Status: fixed in `a8241a1` (GitHub issue #8).** The text below tells what went wrong, why, and
how we fixed it.

## Background for beginners

Read this section if you are new to this project.

**What the orchestrator does.** The orchestrator is the agent loop. In each round, it does these
steps:

1. The agent proposes a design configuration, for example 128 neurons at a 40 ns clock.
2. The orchestrator writes the design files into a run directory.
3. It runs a simulation that compares the design with a golden model.
4. It runs the place-and-route flow (PnR) in a docker container. The flow makes the chip layout
   and measures power, timing and area.
5. It writes one line to `journal.jsonl`. The line holds the configuration and the results.

The agent reads the journal to decide the next configuration. Engineers read the journal as
evidence. Thus each journal line must be correct, and we must know which run wrote it.

**Why runs overlap.** One PnR run of a 128-neuron design takes 43 to 55 minutes. During that
time, it is easy to start a second run, for example a test with a different configuration.

## Symptom

Two runs of the orchestrator wrote to one directory at the same time. Neither run reported an
error. The journal then held lines from both runs. A reader could not tell which line belonged to
which run.

The observed case gave a timeline that looked impossible:

- One journal line recorded a failure after 3.4 seconds.
- Another line recorded a different verdict 15 minutes later.
- A container did real work for 25 to 52 minutes in the same window.

All three facts were true. They belonged to two different runs.

## Root cause

The orchestrator wrote every run into `runs/<target>/round_N` and took no lock on that path.
Thus a second run wrote over the design files of the first run while the first run still read
them. The design files in the observed case had the time stamp of the second run.

Both runs also added lines to one journal and wrote to one results tree. Each run reported its own
verdict, so each verdict looked independent. Neither run could see the other run.

## Why this matters

The journal is the evidence for every investigation. A journal that mixes two runs without a sign
is worse than a weak record. It is a misleading record, because each line looks correct alone.
This fault made us lose the evidence for one hypothesis (H6).

## Fix

We had two possible fixes:

| Fix | Result | Problem |
|---|---|---|
| A lock on the run directory | The second run stops. | The evidence of the second run is lost. |
| One subdirectory for each run | Both runs continue and do not touch each other. | None found. |

We used the second fix. `a8241a1` makes these changes:

1. Each orchestrator run gets a random 8-character identifier, for example `f6599c24`.
2. Each run writes into its own directory: `<out>/<target>/round_N/inv_<id>/`.
3. Each journal line has an `inv` field with the identifier.

Now two runs can share one journal. The `inv` field tells you which run wrote each line.

## Regression test

`tests/test_orchestrator.py::test_concurrent_invocations_isolated_run_dirs_and_journal_lines`
starts two runs. It asserts that each run has its own directory and that each journal line has
an `inv` field. CONFIRMED: the test fails on the old code with `KeyError: 'inv'` and passes after
the fix.

A live test with 2 real processes gave 0 journal lines without `inv`.

## Workaround

None is necessary after `a8241a1`. For a journal line from before 2026-10-17 03:52, check the
time stamps and the running containers before you use the line as evidence. Those lines have no
`inv` field.

## See also

- [ENG-003: tail without pipefail hides a make failure](../incidents/003-tail-without-pipefail.md)
- [ENG-005: make run in the ORFS image is a per-stage noop](../incidents/005-orfs-make-run-is-per-stage-noop.md)
- [ENG-009: PnR results never reached the host](../incidents/009-copy-out-path-and-no-metadata.md)
- [Synthesis load_design failure investigation](../tasks/hypothesis/2026-10-17-1-synth-load-design-fail.md)

## Notes

**Lesson for beginners.** This defect is in one family with ENG-003, ENG-005 and ENG-009. Each
member reported a result that the work did not support:

- ENG-003 reported success for a failed command.
- ENG-005 reported success for work that it did not do.
- ENG-009 reported success for a copy that failed.
- This defect reported two verdicts for one directory.

An agent loop trusts its own reports. Thus a false report costs more than a normal defect. When
you add a step to the flow, make sure that the step reports its failure.
