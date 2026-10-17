---
title: Hypothesis set: 1_synth load_design failure (attempt 3)
created: 2026-10-17
updated: 2026-10-17
type: task
status: open
tags: [flow, orfs, yosys]
sources: []
---

# Hypothesis set: 1_synth load_design failure (attempt 3)

Date: 2026-10-17. Subject: orchestrated 128-neuron PnR run, attempt 3,
fails at `do-1_synth`, last visible line is
`load_design 1_2_yosys.v 1_2_yosys.sdc` at `flow/scripts/synth_odb.tcl`
line 5. The reason string truncation hides the inner error; a full-log
rerun is in flight. Hypotheses below are ranked by existing evidence; each
names the bug page it links to, or "new" if it needs its own incident page.

## Evidence already in hand

- Staged SDC is the fixed form: `create_clock -name clk -period 40.0 [get_ports clk]`
  (bare, no braces). Commit 34c2b1a.
- Attempt 2 (braced SDC) failed at the same make target with
  `ERROR STA-0132 pin '[get_ports' not found` confirmed by the grep-filtered
  debug rerun.
- Attempt 3 failed with the same outer tail, and the failure elapsed time
  matched attempt 2 (yosys work of ~3 s), so the failure is at the same
  early point of the stage.
- Full-log rerun pending; nothing below is confirmed yet.

## Hypotheses

### H1. STA-0132 persists despite the brace fix (stale or wrong SDC reaching read_sdc)

- Claims: the file read by `read_sdc` is not the file we staged (stale copy
  inside the image tree, or a second SDC path wins in the makefile), so the
  braced form is still being parsed.
- Links to: ENG-008 (pending page, SDC braces) and ENG-005 class (a stale
  artifact surviving a fix).
- Confirm/kill: the full log's ERROR STA lines; `grep get_ports` on
  `flow/results/sky130hs/snn_core_128/base/1_2_yosys.sdc` inside the
  container after the run.
- Prior: low. Staged file verified bare before launch.

### H2. Missing `current_design` in the SDC makes read_sdc resolve pins against no design

- Claims: ORFS example SDCs begin `current_design gcd`; ours has only
  `create_clock`. If `load_design` reads the netlist but the SDC is parsed
  before the design binds, `[get_ports clk]` can fail a different way than
  the pin-not-found text.
- Links to: ENG-008 (same SDC page, second contributing defect).
- Confirm/kill: full log STA-0132 text; add `current_design snn_core_128`
  and rerun synth only.
- Prior: medium. Cheap to test, canonical ORFS form includes it.

### H3. Yosys netlist instantiates cells with no sky130 LEF master (ORD-2013 class)

- Claims: unmapped or blackboxed instances (memory arrays inferred from
  `v[]`/`acc[]`, generate-scope logic, latch inference) reach the netlist;
  `read_db`/`read_lef` at load_design cannot find a master and the open
  upstream issue (OpenROAD #9413) makes that a hard error since commit
  435cbd5d.
- Links to: new bug page (first occurrence is this run) referencing
  upstream OpenROAD issue 9413.
- Confirm/kill: full log for `ORD-2013` or `STA-0198 ... Creating black
  box`; `yosys -p "stat"` on the design, or grep `1_2_yosys.v` for cell
  prefixes the sky130 LEF does not define.
- Prior: medium-high. The netlist load IS the failing step, and this is the
  documented failure class at exactly that step.

### H4. The synth stage produced no netlist and a make-level noop reported success (ENG-005 fault class again)

- Claims: `do-yosys` exited 0 while producing a broken or empty
  `1_2_yosys.v`, then `load_design` fails with "cannot open" (STA-0132's
  sibling sta_error 340, which the grep-filtered run already surfaced
  once).
- Links to: ENG-005 (per-stage success without artifacts) and ENG-003
  (exit-code laundering through pipeline/make chains).
- Confirm/kill: full log for `sta_error 340` / `cannot open`; check
  `1_2_yosys.v` size in the results tree.
- Prior: medium. The 340 line has surfaced once in filtered output
  already.

### H5. Our generated RTL trips a yosys memory-detection path that ORFS's parallel-synth memory extraction mishandles

- Claims: `v` and `acc` are `reg signed [ACC_W-1:0] v [0:PAD-1]`, indexed
  by constant generate loops; `extract_memories.tcl` or `memories.json`
  handling sees them as RAM macros instead of flip-flop banks, and the
  load fails when OpenDB cannot build the macro.
- Links to: new bug page (would be our first generator-RTL-caused flow
  failure, distinct from ENG-004 which was a testbench range bug).
- Confirm/kill: grep full log for `memories` / `memories.json` lines;
  inspect `flow/results/.../memories` presence; compare with a minimal
  4-neuron config.
- Prior: low-medium. The arrays are written only in constant-index loops,
  so yosys should map to DFFs, but the ORFS memory pipeline is the least
  verified part of the image.

### H6. Nothing new: the reason string is stale because the run reused attempt 2's results

- Claims: attempt 3's journal line is a copy of attempt 2's failure
  (identical elapsed times raised this), i.e. the flow never actually
  reran with the fixed SDC.
- Links to: ENG-006 (the results mount) and ENG-003 (stale-dir purge now
  protects against same-name reuse; if purged, this hypothesis dies).
- Confirm/kill: journal line count (3 lines for 3 attempts, checked), the
  staged SDC content (bare, checked), container duration (25+ min of
  making observed). Mostly killed already; a 4th check is whether attempt
  3's docker actually pulled the freshly staged file (mount path identical
  to attempt 2, high confidence it did).
- Prior: very low. Listed for completeness because the coincidence of
  identical elapsed times was genuinely suspicious.

### H7. KILLED: liberty/LEF mismatch (platform variant mixing), proposed and killed same day

- Proposed by the peer session on the same run: sky130 standard cells from
  a different variant than the LEF would give load_design masters it
  cannot resolve (same ORD-2013 class as H3).
- Killed with image-filesystem evidence, not journal evidence: inside
  image d4590b320d36, `flow/platforms/sky130hs/config.mk` is internally
  consistent: TECH_LEF `sky130_fd_sc_hs.tlef`, SC_LEF
  `sky130_fd_sc_hs_merged.lef`, LIB_FILES
  `sky130_fd_sc_hs__tt_025C_1v80.lib`, all `_hs_` and all resolved from
  PLATFORM_DIR. No mixing exists. This kill is sound (config content is
  not attributable to concurrent writers; it is an invariant of the image)
  and survived the attribution sweep.

## Addendum: attribution sweep (2026-10-17, later same day)

The journal recorded four lines for this set, but the run directory had
two concurrent writers (see wiki/bugs/orchestrator-run-dir-has-no-lock.md),
so journal attribution is unsound for every line written while both ran.
Consequences for the set, per the killed-versus-did-not-reproduce rule:

- **H6 kill evidence retracted.** The kill rested on journal line count
  (3 lines for 3 attempts) and on facts "observed" during the attempt-3
  window (staged SDC content, 25 minutes of making). None of that is
  attributable to a specific invocation while a second writer was live.
  H6 returns to open with no kill evidence; the identical-elapsed-time
  suspicion that motivated it is itself explainable by a second writer
  reporting into a shared directory.
- **H4's supporting line downgraded.** The sta_error 340 cannot-open line
  surfaced once in grep-filtered output during the attempt-3 debugging
  window. That window overlaps the second writer's activity, and line 2's
  failure itself (`cp: cannot stat ... No such file or directory` after a
  3.4 s synth) is confounded by a plausible concurrent-staging-overwrite
  mechanism. Provenance unknown: absence of attribution is absence of
  evidence, so H4 stands on its mechanism argument only. Confirm/kill is
  unchanged: one `yosys> stat` and the `1_2_yosys.v` size check.
- **Attempt-3 failure did not reproduce.** A rerun with identical staging
  (bare `[get_ports]` SDC, DESIGN_NAME snn_core_128, same 40 ns clock)
  passed synth, CTS, and reached routing with no ERROR lines in 114 KB of
  log. Recorded as did-not-reproduce, not a kill: absence of evidence.
  Status stays open.
- **Lines 0-1 attribution.** No evidence of a second writer during those
  windows (the second writer's first traceable footprint is the 02:11:57
  staging mtime; lines 0-1 correspond to the docker-125 and DESIGN_NAME
  defects fixed one by one before that). But "no evidence of overlap" is
  weaker than "single writer": the journal cannot distinguish writers at
  all until the invocation-id fix lands.
- **Tail property.** The identical outer tails across attempt failures
  (and the identical elapsed times) are properties of the reporting layer
  (reason-string truncation), never evidence of a matching cause. Same
  finding generalized from ENG-003.

## Next actions

1. Full-log rerun finishes; anchor hypotheses H1-H5 to its ERROR lines.
2. Kill or upgrade each to confirmed with the file/line it names.
3. Confirmed winner gets its incident page (ENG-008 family or new), the
   losers stay here with their evidence.
4. Invocation identifier on every journal line (fix for the run-dir bug
   page) before any further journal evidence is recorded.

## Related

- [ENG-003](../../incidents/003-tail-without-pipefail.md),
  [ENG-005](../../incidents/005-orfs-make-run-is-per-stage-noop.md),
  [ENG-006](../../incidents/006-relative-docker-bind-paths.md) and
  [ENG-007](../../incidents/007-design-name-equals-top-module.md) are the
  flow-bug chain this run walked through; references below use the
  wiki/engineering paths valid at the time of writing, wiki layout is
  being migrated by the peer session.
- [Concurrent orchestrator invocations clobber one shared run
  directory](../../bugs/orchestrator-run-dir-has-no-lock.md): the
  two-writers defect that forced the attribution sweep above (page
  written by the peer session, fix owned by targets/).
- [Engineering log procedure](../../procedures/add-an-engineering-log-entry.md)
  names the one-file-per-live-failure convention; its README (folded into
  [wiki/index.md](../../index.md)) is superseded by that page.
- docs/backlog.md is unaffected; this is a debug record, not a direction.
