# Wiki Schema

This LLM-Wiki is managed by the `wiki` skill created by Andreas F. Hoffmann from the `knowledge_management` plugin in [theafh AI-repo](https://github.com/theafh/ai-modules).

## Domain

Engineering incident records and procedures for the agentic SNN chip design project. Incident reports document bugs, limits, and decisions with their symptoms, root causes, fixes, and regression tests. Procedures document rules and workflows for adding entries to the log.

## Conventions

- **Folder layout is the type axis only.** Every page lives directly at
  `<pluralized-type>/<slug>.md`, flat, one layer deep (`incidents/001-np-diag-returns-1d.md`,
  `procedures/add-an-engineering-log-entry.md`). No thematic prefix folders, no sub-folders inside a type
  folder, no pages at the wiki root. Thematic scope is expressed through `tags:`
  and `type:`, both of which have explicit declared sets in this schema; the
  folder tree does not carry a second axis. The linter blocks misfiled pages and
  warns when a declared type folder is missing on disk.
- File names: lowercase, hyphens, no spaces (e.g., `add-an-engineering-log-entry.md`)
- Every wiki page starts with YAML frontmatter (see below)
- Cross-link with standard relative markdown links: `[index](../index.md)`
  from a different folder, `[other-incident](001-np-diag-returns-1d.md)` from the same folder.
  Minimum 2 outbound links per page.
- When updating a page, always bump the `updated` date
- Every new page must be added to `index.md` under the correct section
- Every action must be appended to `log.md`
- **Provenance:** this is an LLM-first wiki. Attribution belongs *next to*
  the claim it attributes, not collected at the bottom of the page. The
  `sources:` frontmatter is the canonical list of every raw file the page
  draws on. Pages do not carry a body "Sources" section. Per-claim attribution uses inline
  standard-markdown links: 
  ```markdown
  The fix landed in commit ([3dd7a68](../index.md)).
  ```
  Footnote markers are not used.

## Frontmatter

```yaml
title: Page Title
created: YYYY-MM-DD
updated: YYYY-MM-DD
type: incident | procedure
tags: [from taxonomy below]
sources: []
```

For incident pages, `sources` should list the real files cited (e.g., commits, test files, source files).
For procedure pages, `sources` should be an empty list unless the procedure is derived from external material.

## Tag Taxonomy

- Issues: bug
- Components: photonic, testbench, flow
- Techniques: numpy, cocotb, orfs, makefile, docker, yosys
- Meta: regression-test

Rule: every tag on a page must appear in this taxonomy. If a new tag is needed,
add it here first, then use it.

Tags for future use: `limit` for operational limits, `decision` for documented choices, `golden-model` for golden model issues.

## Linter Notes

The linter is `scripts/lint.py` in the `knowledge_management` plugin. Run it with this directory as
the positional argument. It reports and does not change files.

Three constraints are easy to break by habit:

- Do not put a horizontal rule in the body of a page. The linter reads a line of three dashes as a
  list marker without a space after it. Separate a footer with a blank line instead.
- Give every fenced code block a language identifier. Use `shell` for a command and `python` for
  Python code or a Python error.
- Give every page at least two outbound links to other pages, and list every page in `index.md`. A
  page with no inbound link is an orphan and the linter warns about it.

This wiki holds zero em dashes and zero en dashes, which is a project rule and not a linter rule. The
linter does not check it. Check it by codepoint, because an editor can insert one silently.

## Page Types

| Type | Purpose |
| --- | --- |
| **incident** | A bug, limit, or decision with symptom, root cause, fix, and regression test |
| **procedure** | A rule or workflow for how to act in this domain |

## Incident Pages

Answers "what happened, why, and how was it fixed?" One page per bug, limit, or decision. Include:

- Symptom: what a person sees when the fault happens
- Root cause: why the fault happens, with file names and line numbers
- Fix: what changed and where
- Regression test: the test that fails if the fault returns
- Notes (optional): anything a future reader needs

## Procedure Pages

Answers "how should this be done?" One page per rule or workflow. Include:

- Title at H1 with one-paragraph summary stating the rule and scope
- When this applies: the trigger or context
- The rule or steps
- Pitfalls or edge cases (optional)
- See also: links to related pages and worked examples

## Update Policy

When new information conflicts with existing content:

1. Check the dates. Newer sources generally supersede older ones
2. If genuinely contradictory, note both positions with dates and sources
3. Update the `updated` date field

[Wiki index](../README.md)
