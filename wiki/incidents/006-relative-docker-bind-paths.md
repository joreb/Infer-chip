---
title: relative docker bind paths are rejected as named volumes
created: 2026-10-17
updated: 2026-10-17
type: incident
tags: [bug, flow, docker, regression-test]
sources: []
---

# ENG-006: relative docker bind paths are rejected as named volumes

Text written in ASD-STE100 Simplified Technical English.

| Field | Value |
|---|---|
| ID | ENG-006 |
| Kind | bug |
| Status | fixed |
| Area | flow (targets/digital/flow.py, run_pnr docker command) |
| Fix commit | `0090dc2` |
| Pinned by | `tests/test_review_fixes.py::test_run_pnr_mounts_are_absolute` |

## Symptom

The orchestrated digital flow run failed before make started. The journal reason was
`orfs make exited 125:` followed by empty output, because the old reason string only
carried stdout and docker writes its errors to stderr. After stderr joined the reason
string, the real message appeared, quoting the daemon:

```text
docker: Error response from daemon: create runs_digital_e2e/digital/round_0/orfs:
"runs_digital_e2e/digital/round_0/orfs" includes invalid characters for a local volume
name, only "[a-zA-Z0-9][a-zA-Z0-9_.-]" are allowed. If you intended to pass a host
directory, use absolute path
```

## Root cause

`targets/digital/flow.py` built the two bind mounts from the caller's `out_dir` value.
The orchestrator passes a relative path such as `runs_digital_e2e/digital/round_0`, so
the docker command held `-v runs_digital_e2e/digital/round_0/orfs:/mnt/design`. A docker
`-v` left side holds either an absolute host path or a named volume name. Without a
leading slash docker takes the second reading, and a path with slashes is an invalid
volume name.

The manual reproduction commands worked the whole time, because they were typed with
absolute `/mnt/d/...` paths. The orchestrator was the only caller that ever held a
relative path, so the fault hid until the real loop ran it.

## Fix

Resolve both mount sources to absolute paths before the command is built:

```python
results_host.mkdir(parents=True, exist_ok=True)
docker_cmd = [
    "docker", "run", "--rm", "-u", "0:0",
    "-v", f"{stage_dir(out_dir).resolve()}:/mnt/design",
    "-v", f"{results_host.resolve()}:/results",
    IMAGE, "bash", "-c", cmd,
]
```

The `mkdir` exists because docker creates a missing host bind source as an empty
directory owned by root, which is a second trap on the same line.

## Regression test

`tests/test_review_fixes.py::test_run_pnr_mounts_are_absolute` records the docker
command with a fake subprocess, passes a relative `out_dir`, and asserts both `-v`
sources start with `/`. CONFIRMED: the assertion fails on the pre-fix code, where the
sources are the raw relative paths.

## Notes

Same investigation as [ENG-005](005-orfs-make-run-is-per-stage-noop.md) and
[ENG-007](007-design-name-equals-top-module.md), which went to make and yosys instead
of stopping here. See also [index](../index.md) and
[procedure](../procedures/add-an-engineering-log-entry.md).
