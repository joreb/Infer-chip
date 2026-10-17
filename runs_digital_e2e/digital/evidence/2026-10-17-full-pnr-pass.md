# First full PnR pass: 128-neuron snn_core_128 on ORFS sky130hs

Date: 2026-10-17. Config: neurons=128, fanout=8, weight_width=4,
timesteps=64, util_target=25, clock_ns=40.0 (journal rounds record).
Image: openroad/orfs:latest d4590b320d36. Verbatim log:
`2026-10-17-full-pnr-pass.log` (142 KB, zero ERROR lines, rc=0).

## Numbers (extracted from the log; metadata.json lost with --rm, see note)

| Metric | Value | Log line |
|---|---|---|
| Verdict | pass (rc=0, GDS merged: 6_1_merged.gds -> 6_final.gds) | cp line, final |
| Setup slack (FLW-0009, clock clk) | +32.682 ns at 40 ns period | FLW-0009 |
| Setup violations | none (RSZ-0098) | line 1100 |
| Hold violations | none (RSZ-0033) | line 1602 |
| DRC violations | 0 (DRT-0199 final pass = 0) | line 2366 |
| Antenna violations | 0 nets / 0 pins (ANT-0001/-0002) | lines 2415-2418 |
| Design area | 704933 um^2 (0.705 mm^2), 28% utilization | "Design area" x3 |
| Stdcell count | 4382 sequential, 45336 multi-input comb, 1100 timing-repair buffers, 694 clock buffers, 1927 inverters, 280035 cells incl. 198879 fillers + 27303 taps | cell type report |
| Instance area incl. fill/tap | 2527477.99 um^2 | cell type report |
| Total power | 1.42e-02 W = 14.2 mW | PSM IR report |
| IR drop (VDD) | worst 5.93e-05 V, 0.00% | PSM report |
| Wirelength | 1449559 um (met1 760503, met2 629374, met3 36132, met4 23127, met5 422) | DRT layer report |
| Wall time | 55 min (container 03:05-04:00 CEST) | docker ps span |
| Peak memory | 3455 MB (route), 2.66 GB (finish) | stage table |

## Note on provenance

The flow's copy-out (`cp -r flow/results/... /results/`) never reached the
host: the bind target was empty after container exit and no docker volume
was created, so `metadata.json` and `6_final.gds` were lost with `--rm`.
Every number above is quoted from the merged stage log with its line
evidence. Until a rerun captures the results tree, metrics that parse_metrics
reads (instance__area__stdcell, worst setup slack from metadata) are not
re-derivable from this record; the FLW-0009 and cell-type-report lines are.

## Provenance caveat (journal attribution)

This run was a single-writer window: the only live writer was the rerun
container plus a snapshot-copy loop that later proved to be a no-op (its
docker cp errors were redirected to /dev/null, and docker cp does not
create the intermediate destination directory). No journal line was
written for this run. If it is re-orchestrated, the inv-stamped journal
records it normally.