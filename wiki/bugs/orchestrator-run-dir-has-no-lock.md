---
title: Concurrent orchestrator invocations clobber one shared run directory
created: 2026-10-17
updated: 2026-10-17
type: bug
tags: [flow, testbench]
sources: []
---

# Concurrent orchestrator invocations clobber one shared run directory

Text written in ASD-STE100 Simplified Technical English.

## Symptom

Two runs of the orchestrator write to one directory at the same time. Neither run reports an error.
The journal then holds lines from both runs, and a reader cannot tell which line belongs to which run.

The observed case produced a timeline that looked impossible. One journal line recorded a failure after
3.4 seconds. Another line recorded a different verdict 15 minutes later. A container did real work for
25 to 52 minutes in the same window. All three facts were true, and they belonged to two different
runs.

## Root cause

The orchestrator stages every run into `runs/<target>/round_N` and takes no lock on that path. A
second invocation therefore rewrites the staged input files of a first invocation while the first
invocation still reads them. The staged files in the observed case carried the modification time of
the second launch.

Each run also appends to one shared journal and writes to one shared results tree. Each run reports
its own verdict, so each verdict looks independent. Neither run can detect the other.

## Why this matters more than one wrong timeline

The journal is the evidence that every investigation reads. A journal that silently mixes two runs is
not a weak record. It is a misleading record, because each line looks authoritative on its own.

Any evidence line from a window with concurrent runs needs a check for attribution before anybody
uses it. That applies to evidence already recorded, not only to new evidence.

## Workaround

Run one invocation at a time. Before a run, check for a running container and for a background shell
that targets the same round directory.

## Proposed fix

Two options, and they solve different problems.

A lock on the run directory stops the second invocation. It prevents the corruption, and it also
destroys the evidence of the second run.

A per-invocation subdirectory under the round directory lets both runs proceed without contact. Each
run keeps its own staged files, its own results and its own journal lines. Concurrency then becomes
harmless rather than forbidden.

The second option suits a debugging workflow better, because the evidence of both runs survives. Add
an invocation identifier to every journal line as well. The failure then explains itself in the record
instead of needing a reconstruction.

## See also

- [ENG-003: tail without pipefail hides a make failure](../incidents/003-tail-without-pipefail.md)
- [ENG-005: make run in the ORFS image is a per-stage noop](../incidents/005-orfs-make-run-is-per-stage-noop.md)
- [Synthesis load_design failure investigation](../tasks/hypothesis/2026-10-17-1-synth-load-design-fail.md)

## Notes

This defect belongs to a family with ENG-003 and ENG-005. Each member of the family reports a result
that the work does not support. ENG-003 reported success for a failed command. ENG-005 reported
success for work it never did. This defect reports two verdicts for one directory. A verification loop
depends on its own reports, so this family costs more than an ordinary defect.
