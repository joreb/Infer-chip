# Orchestrated 128-neuron PnR pass with all files on the host (#1)

Text written in ASD-STE100 Simplified Technical English.

Date: 2026-10-18. Commit: dfef3b6 (flow fix) plus the `parse_metrics`
stage fix in the same issue. Image: `openroad/orfs:latest` d4590b320d36.
Config: neurons=128, fanout=8, weight_width=4, timesteps=64,
util_target=25, clock_ns=40.0 (the same as the run of 2026-10-17).

Command: `orchestrator.py --target digital --rounds 1 --out runs_e2e128`.
The full `docker run` command is in `2026-10-18-docker_cmd.txt`. The
journal line is in `2026-10-18-journal-line.json` (`inv = f6599c24`).
The full metadata is in `2026-10-18-metadata.json`.

## Pass metrics of #1

| Metric | Pass value | Measured |
|---|---|---|
| `metadata.json` on the host | exists, size > 0 | 26,304 bytes |
| `6_final.gds` on the host | exists, size > 0 | 69,171,790 bytes (sha256 1c22111daa085f09…) |
| Stage logs on the host | exist | 23 logs |
| Journal line | 1, with `inv`, `flow.verdict = pass` | 1, `inv = f6599c24`, pass |
| DRC violations | 0 | 0 |
| Setup slack at 40 ns | ≥ 0 ns | +33.1432 ns (finish) |
| Agreement with 2026-10-17, same measurement | within 1% | 0.00% on all five metrics |

Wall time: 43 min (11:38 to 12:21 CEST).

## Same measurement, two runs

| Metric | Metadata key | 2026-10-17 (stage log) | 2026-10-18 (metadata) |
|---|---|---|---|
| Design area | `finish__design__instance__area__stdcell` | 704933 um² | 704933 um² |
| Wirelength | `detailedroute__route__wirelength` | 1449559 um | 1449559 um |
| Global-route slack | `globalroute__timing__setup__ws` (FLW-0009) | 32.682 ns | 32.682 ns (log), 32.6825 (metadata) |
| Total power | `finish__power__total` | 1.42e-02 W (PSM, 3 digits) | 1.41645e-02 W |
| DRC | `detailedroute__route__drc_errors` | 0 | 0 |

The two runs give the same result. The flow is deterministic for this
config and image.

## Two corrections to the evidence of 2026-10-17

1. **The slack value is the global-route slack, not the final slack.**
   FLW-0009 prints at the global-route stage. The final (finish) setup
   slack is +33.1432 ns. Both are positive, so the timing verdict does not
   change.
2. **The copy-out cause.** See the correction in
   `2026-10-17-full-pnr-pass.md`: the cause was the `cd flow` path defect
   in `flow.py`, not the manual wrapper.

## Defect found by this run

`parse_metrics` took the first key that matched each pattern. Real
metadata repeats each metric at each stage, and `cts__` keys come before
`finish__` keys. Thus the agent got CTS-stage values: slack 33.1717 and
wirelength 1282660 (a CTS estimate, 11.5% lower than the routed value).
The fix names the final-stage keys first. The test
`test_parse_metrics_picks_final_stage_values_from_real_metadata` uses this
run's metadata as its fixture. It failed before the fix and passes after
it.

The GDS (69 MB) is not in git. It is at
`runs_e2e128/digital/round_0/inv_f6599c24/final.gds`.
