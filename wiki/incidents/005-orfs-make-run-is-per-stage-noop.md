---
title: make run in the ORFS image is a per-stage noop that returns rc=0
created: 2026-10-17
updated: 2026-10-17
type: incident
tags: [bug, flow, orfs, makefile, regression-test]
sources: []
---

# ENG-005: make run in the ORFS image is a per-stage noop that returns rc=0

Text written in ASD-STE100 Simplified Technical English.

| Field | Value |
|---|---|
| ID | ENG-005 |
| Kind | bug |
| Status | fixed |
| Area | flow (targets/digital/flow.py) |
| Fix commit | 073b376 |
| Pinned by | `tests/test_review_fixes.py::test_run_pnr_uses_pipefail_and_purges_stale_results` |
| Observed on | openroad/orfs:latest, image id `d4590b320d36` (pulled 2026-10-16) |

## Symptom

A PnR run finished in less than a second and printed `make -C flow DESIGN_CONFIG=... run`
as its last output, but the results tree was empty. No GDS, no metadata.json, no logs.
The command exited 0. Earlier stage of the same investigation showed `run` as the make
target name in the flow docs, so the target looked right.

The run also wrote nothing to the journal past the invocation line, because
`parse_metrics` found no metadata.json. That is the detector that caught the fault: a
command that reports success for work it did not do.

## Root cause

In the openroad/orfs image, `run` is not the flow target. It is a per-stage helper at
`flow/Makefile:915` that executes one openroad invocation taken from the `RUN_SCRIPT`
environment variable. When `RUN_SCRIPT` is not set, the helper runs a single openroad
noop and returns rc 0. It never touches the results tree.

The full flow is the default goal, defined separately from `run` in the same makefile:
`all: check-yosys check-openroad synth floorplan place cts route finish`.

So an invocation of the shape `make DESIGN_CONFIG=... run` asked a helper to run with no
script. The helper did exactly what the makefile says and exited clean.

## Fix

Invoke the default goal. The command in `run_pnr` is now
`make DESIGN_CONFIG=./designs/<platform>/<design>.mk 2>&1 | tail -5` with no target name,
which resolves to `all`. Verified against the image id above.

## Regression test

`tests/test_review_fixes.py::test_run_pnr_uses_pipefail_and_purges_stale_results`
asserts that the docker command contains
`make DESIGN_CONFIG=./designs/sky130hs/snn_core_32.mk` and that `.mk run ` does not
appear in it. It also asserts that results from a stale earlier run are removed before
the command starts.

The stronger guard for this fault class is the empty-results check, not the string
assertion. `parse_metrics` returns `{"verdict": "fail", "reason": "no metadata.json
found under results dir"}` when the flow produced nothing, so a silent success with an
empty tree becomes an honest fail in the journal. CONFIRMED: with a fake `make` that
writes nothing, the metrics step returns the fail verdict above.

## Masked window

The window where results could be falsely empty is 50ea631 (flow wrapper with the
`run` target) to 073b376 (fix). Every journal entry for a run inside that window has
flow verdict `fail`, because `parse_metrics` rejected each empty tree. No flow metrics
entry from that window exists in any journal under `runs/` or `runs_digital_e2e/`, so
no journalled number needed a flag.

## Notes

Same fault class as ENG-003, different mechanism. ENG-003 is a pipeline that hides an
exit code. This one is a target that does less work than its name promises and exits
clean. In both cases the command did not report the fault, and the detector was
downstream. General rule for this flow: a stage ends in pass only when a result
artifact exists, never on exit code alone.

See also [index](../index.md), [ENG-003](003-tail-without-pipefail.md), and [procedure](../procedures/add-an-engineering-log-entry.md).

## See also

- [Synthesis load_design failure investigation](../tasks/hypothesis/2026-10-17-1-synth-load-design-fail.md). This hypothesis set tests the same fault class again under a different scenario.
