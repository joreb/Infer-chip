# Engineering log

Text written in ASD-STE100 Simplified Technical English.

This part of the wiki holds our own work. The other parts of the wiki hold summaries of external
sources. Keep the two apart, because the engineering log is a record of what happened in this project
and nobody else is the authority on it.

One page holds one incident. A page holds the symptom, the root cause, the fix and the regression test
together. Do not split those four parts across separate folders.

Why one page. A bug, its fix and the test that pins it are one story. A reader who finds the symptom
needs the fix in the same place. Three folders hold three copies of the same story, and the copies drift
apart as soon as somebody edits one of them.

Use the index below for the views that separate folders would have given. The Kind column and the
Status column answer "show me the open bugs" and "show me the decisions" without a second copy of the
text.

## Entries

| ID | Title | Kind | Status | Pinned by |
|---|---|---|---|---|
| ENG-001 | np.diag on a 2-D matrix returns the 1-D diagonal | bug | fixed | `tests/test_mesh.py::test_diag_encode_stays_2d` |
| ENG-002 | cocotb results parser lives in check_results and returns a 2-tuple | bug | fixed | `tests/test_review_fixes.py::test_sim_parity_non_pow2_neurons` |
| ENG-003 | tail without pipefail hides a make failure | bug | fixed | `tests/test_review_fixes.py::test_run_pnr_uses_pipefail_and_purges_stale_results` |
| ENG-004 | testbench inject loop over PAD raises IndexError at a non-power-of-two neuron count | bug | fixed | `tests/test_review_fixes.py::test_sim_parity_non_pow2_neurons` |

## How to add a page

1. Copy `_template.md` to `NNN-short-slug.md`. Use the next free number.
2. Fill every field in the table at the top. Write `n/a` where a field does not apply.
3. Add one row to the index above.
4. Name the identifier in the test itself, for example `# pins ENG-003`. A reader of the test then finds
   the page, and a reader of the page finds the test. Without that comment the link breaks the first
   time somebody renames the test.

## Rules for a page

- Write the symptom before the cause. A reader arrives with the symptom, not with the cause.
- Quote the real error text. Do not paraphrase an error message.
- Name the file and the line of the root cause.
- State what the regression test asserts, and state whether the test was confirmed to fail on the old
  code. An unproven regression test gives false confidence.
- A page that records a deliberate limit instead of a defect uses Kind "limit". Give the condition under
  which the limit stops being acceptable.
- Use ASD-STE100 Simplified Technical English. Use no em dashes and no en dashes.

---
[Wiki index](../README.md)
