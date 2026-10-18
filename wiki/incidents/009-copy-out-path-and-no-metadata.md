---
title: PnR results never reached the host and metadata.json was never written
created: 2026-10-18
updated: 2026-10-18
type: incident
tags: [bug, flow, docker, orfs, regression-test]
sources: []
---

# ENG-009: PnR results never reached the host and metadata.json was never written

Text written in ASD-STE100 Simplified Technical English.

| Field | Value |
|---|---|
| ID | ENG-009 |
| Kind | bug |
| Status | fixed |
| Area | flow (`targets/digital/flow.py`, container script of `run_pnr`) |
| Fix commit | `dfef3b6` |
| Pinned by | `tests/digital/test_flow_parse.py::test_container_script_puts_gds_metadata_and_logs_on_the_host` |

## Background for beginners

Read this section if you are new to chip design. Skip it if you know ORFS.

**What the flow does.** A chip design starts as Verilog text. Verilog describes the logic. A
"place and route" flow (PnR) turns the logic into a physical layout. The flow does these stages
in this order:

1. **Synthesis.** It changes the Verilog into a netlist of standard cells (small logic gates from
   the cell library).
2. **Floorplan and placement.** It puts each cell at a position on the die.
3. **Clock tree synthesis (CTS).** It adds buffers so that the clock gets to every flip-flop at
   the same time.
4. **Routing.** It connects the cells with metal wires. Global routing makes a plan. Detailed
   routing draws the real wires.
5. **Finish.** It writes the final layout file, `6_final.gds`. A chip factory makes the chip from
   this file.

We use OpenROAD-flow-scripts (ORFS) on the sky130hs cell library. ORFS runs inside a docker
container from the image `openroad/orfs`.

**What a container is.** A container is a small isolated computer. It has its own files. Our
command starts it with `--rm`. Thus docker deletes the container and all its files when it
stops. Only files in a "bind mount" stay. A bind mount connects one host directory to one
directory in the container. We mount the host directory `results/` at `/results`. Each file that
the script copies to `/results` stays on the host.

**What the agent needs.** The agent loop reads the PPA numbers after each run. PPA means power,
performance (timing slack) and area. ORFS writes these numbers into `metadata.json`. Without this
file, the agent gets no feedback.

## Symptom

The 128-neuron run of 2026-10-17 passed. The stage log showed rc=0 and a merged GDS. But after
the container stopped, the host `results/` directory was empty. `6_final.gds` was lost.
`parse_metrics` returned this verdict:

```text
no metadata.json found under results dir
```

The script did not report an error. The container exit code was 0.

## Root cause

There were two separate faults in the script that `run_pnr` gives to the container.

**Fault 1: the copy used the wrong path.** The old script was:

```text
cd flow && make DESIGN_CONFIG=./designs/sky130hs/<name>.mk 2>&1 | tail -5; ...
cp -r flow/results/sky130hs/<name> /results/<name>; ...
```

In bash, `cd` stays in effect for all later commands on the same line. After `cd flow`, the path
`flow/results/...` points to `flow/flow/results/...`. That directory does not exist. `cp`
failed with `cp: cannot stat`. The script did not check the `cp` exit code, so it still exited
0. The wrong assumption: "each command starts from the ORFS root directory."

**Fault 2: `metadata.json` was never written.** A bare `make` runs the PnR stages only. It does
not run the metrics step. ORFS writes `metadata.json` only from the target
`make metadata-generate`. It writes the file under `flow/reports/`, not under `flow/results/`.
Thus the file did not exist anywhere, also inside the container. The wrong assumption: "the
flow writes its metrics as part of the normal run."

We first blamed the manual wrapper that started the rerun. That was wrong. The first test of the
mounts did not run `cd flow`, so it did not see Fault 1. We found the real cause when we ran the
real script in `openroad/orfs:latest`.

## Fix

`dfef3b6` moved the script into the function `container_script()` and changed these items:

1. All copy paths are relative to `flow/`, because the script is in `flow/` after `cd flow`.
2. After a good `make`, the script runs `make metadata-generate`.
3. The script copies `results/`, `reports/` and `logs/` to the host. It puts `metadata.json`
   beside the results, where `parse_metrics` looks for it.
4. Each copy has the guard `|| { [ $rc -eq 0 ] && rc=1; }`. A failed copy now makes the script
   fail. It does not hide the first error code.

The same commit fixed three items that the investigation found:

- **No record of the command.** `run_pnr` now writes the full `docker run` command to
  `docker_cmd.txt` in the run directory.
- **A timeout started a second run.** The Python timeout stops the docker client, but the
  container continues. The old code then tried again, so two ORFS runs used the machine. Now the
  container has a name (`orfs-<design>-<8 hex>`). On a timeout, `run_pnr` runs `docker kill` on
  that name and does not try again.
- **The timeout was too short.** A 128-neuron run takes 43 to 55 minutes. The default timeout
  went from 3600 s to 7200 s.

## Regression test

`tests/digital/test_flow_parse.py` holds these tests:

| Test | What it asserts | Fails on old code |
|---|---|---|
| `test_container_script_puts_gds_metadata_and_logs_on_the_host` | Runs the real script under bash. A stub `make` writes the ORFS trees. The GDS, `metadata.json` and a log must be on the "host", and `parse_metrics` must pass. | Yes, confirmed. With the `flow/results` path put back, the test fails. |
| `test_container_script_fails_when_copy_out_fails` | If the flow makes no files, the script exit code is not 0. | Not confirmed against the old code. |
| `test_run_pnr_generates_metadata_and_copies_reports_and_logs` | The command has `metadata-generate`, the reports and logs paths, and `--name`. `docker_cmd.txt` exists. | Not confirmed against the old code. |
| `test_run_pnr_timeout_kills_named_container_and_does_not_retry` | One `docker run`, then one `docker kill` with the same name. | Not confirmed against the old code. |
| `test_run_pnr_default_timeout_covers_a_128_neuron_run` | The default timeout is 7200 s or more. | Not confirmed against the old code. |

**Proof on the real flow.** The orchestrated 128-neuron run of 2026-10-18 (`inv = f6599c24`,
43 min) put these files on the host: `metadata.json` (26,304 bytes), `6_final.gds`
(69,171,790 bytes) and 23 stage logs. DRC was 0. The area, the wirelength and the slack were the
same as the run of 2026-10-17. See
`runs_digital_e2e/digital/evidence/2026-10-18-orchestrated-pnr-pass.md`.

## Notes

**Lesson for beginners.** In a shell script, a command that fails does not stop the script. Check
each step that must work. ENG-003 is the same lesson for a pipe: `make | tail` gives the exit code
of `tail`, not of `make`.

**How to find this type of fault.** Run the real script in the real image, and look at the files
on the host after the container stops. A test that runs a simpler copy of the script can miss the
fault. That is what happened here.

The same run found a second defect in the metric parser. See
[ENG-010](010-parse-metrics-took-cts-stage-values.md).

Related: [ENG-003: tail without pipefail hides a make failure](003-tail-without-pipefail.md),
[ENG-006: relative docker bind paths](006-relative-docker-bind-paths.md),
[index](../index.md), [procedure](../procedures/add-an-engineering-log-entry.md).
