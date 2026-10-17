---
title: tail without pipefail hides a make failure
created: 2026-10-17
updated: 2026-10-17
type: incident
tags: [bug, flow, makefile, regression-test]
sources: []
---

# ENG-003: tail without pipefail hides a make failure

Text written in ASD-STE100 Simplified Technical English.

| Field | Value |
|---|---|
| ID | ENG-003 |
| Kind | bug |
| Status | fixed |
| Area | flow |
| Fix commit | `b4b2e0a` |
| Pinned by | `tests/test_review_fixes.py::test_run_pnr_uses_pipefail_and_purges_stale_results` |

## Symptom

A physical flow run that failed mid way reports success. The docker command returns exit code 0:

```shell
make DESIGN_CONFIG=... run 2>&1 | tail -5   # exit code is tail's, not make's
```

The journal records a pass for a run that produced no final GDS, because a stale results directory
from an earlier config with the same design name also survived and supplied the metrics file.

## Root cause

`targets/digital/flow.py`, the docker command construction. Wrong assumption: the pipeline reports the
failure of the command at its head. A pipeline reports the exit status of its last stage, and the last
stage here is `tail`, which succeeds as long as the stream has content. The mask was active from commit
`50ea631`, the first ORFS docker wrapper, until `b4b2e0a`.

A command that masks a failure is the most expensive class of bug in a verification loop: every later
green result is suspect until the start of the mask is known.

## Fix

`targets/digital/flow.py` line 133 prefixes the shell command with `set -o pipefail`, so the pipeline
reports the first failing stage. The function also deletes a results directory of the same design name
before the run, so metrics from a stale run cannot supply this run.

## Regression test

`tests/test_review_fixes.py::test_run_pnr_uses_pipefail_and_purges_stale_results` fakes the docker
call, plants a stale metadata file, and asserts the run reports `fail` and that the command contains
`pipefail`. The pipefail assertion is confirmed against the old code: `git show b4b2e0a~1:targets/
digital/flow.py` holds zero occurrences of `pipefail`, so the literal assertion fails on the fix's
parent commit. The stale purge assertion is not confirmed against the old code: the test pins the
current behavior together, and the parent commit held no purge to revert to.

## See also

- [index](../index.md)
- [ENG-005: make run in the ORFS image is a per-stage noop](005-orfs-make-run-is-per-stage-noop.md)
- [Concurrent orchestrator invocations clobber one shared run directory](../bugs/orchestrator-run-dir-has-no-lock.md). This bug page records a third member of the same fault family.
- [procedure](../procedures/add-an-engineering-log-entry.md)
