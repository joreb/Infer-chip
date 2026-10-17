---
title: Add an engineering log entry
created: 2026-10-17
updated: 2026-10-17
type: procedure
tags: []
sources: []
---

# How to add an engineering log entry

This procedure documents a bug, a limit, or a decision with its symptom, root cause, fix, and regression test.

Text written in ASD-STE100 Simplified Technical English.

## When this applies

You discovered a bug in the design, you found a limit of the current approach, or you made a deliberate decision that affects future work. You need to record it in this log so that future readers find it.

## The rule

1. Copy the incident template structure (see below).
2. Use the next free number NNN as your incident ID.
3. Create a file `NNN-short-slug.md` in the incidents/ folder. The slug should match the title concisely.
4. Fill every field in the frontmatter (created date, type, tags from SCHEMA.md taxonomy).
5. Fill every field in the status table: ID, Kind, Status, Area, Fix commit, Pinned by.
6. Write the Symptom section: what a person sees when the fault happens. Give the exact error text. Give the command that produces it. Do not explain the cause here.
7. Write the Root cause section: why the fault happens. Name the file and the line. State the wrong assumption in one sentence. If the fault was visible only under one condition, name that condition.
8. Write the Fix section: what changed and where. Keep this short. The commit holds the detail.
9. Write the Regression test section: name the file and the test function. State what the test asserts. If you confirmed that the test fails on the old code, say so. If you did not, write "not confirmed against the old code" here.
10. Add a Notes section if anything a future reader needs to know. Delete this section if it is empty.
11. Add links to index.md and to this procedure page at the bottom of the page.
12. Update index.md to add one row for your incident.
13. Append one entry to log.md recording the new incident.

## Frontmatter fields

| Field | Value | Example |
|---|---|---|
| title | Brief title in plain words | np.diag on a 2-D matrix returns the 1-D diagonal |
| created | Date the bug was discovered or decision made | 2026-10-17 |
| updated | Date the page was last changed | 2026-10-17 |
| type | incident or procedure | incident |
| tags | List from SCHEMA.md Tag Taxonomy | [bug, photonic, numpy, regression-test] |
| sources | List of files cited, or empty list | [] |

## Status table fields

| Field | Value | Options |
|---|---|---|
| ID | Incident identifier | ENG-001, ENG-002, ... |
| Kind | Type of report | bug, or decision, or limit |
| Status | Current state | open, or fixed, or accepted |
| Area | Where the fault lives | golden model, or RTL, or testbench, or flow |
| Fix commit | The commit that fixed it | `<sha>` or n/a |
| Pinned by | The test that keeps it fixed | `path/to/test.py::test_name` or n/a |

## Rules for all entries

- Write the symptom before the cause. A reader arrives with the symptom, not with the cause.
- Quote the real error text. Do not paraphrase an error message.
- Name the file and the line of the root cause.
- State what the regression test asserts. State whether the test was confirmed to fail on the old code.
- A page that records a deliberate limit instead of a defect uses Kind "limit". Give the condition under which the limit stops being acceptable.
- Use ASD-STE100 Simplified Technical English. Use no em dashes and no en dashes.
- Keep the line `Text written in ASD-STE100 Simplified Technical English.` on every page.
- Every page needs at least 2 outbound links to other pages.
- Link incidents related by cause, component, or technique to each other.

## See Also

- [Engineering log index](../index.md)
- [SCHEMA.md](../SCHEMA.md) for the tag taxonomy and domain scope
- Example incidents: [ENG-001](../incidents/001-np-diag-returns-1d.md), [ENG-002](../incidents/002-cocotb-check-results-module.md)
