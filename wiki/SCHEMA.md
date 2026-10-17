# Wiki Schema

This LLM-Wiki is managed by the `wiki` skill created by Andreas F. Hoffmann from the `knowledge_management` plugin in [theafh AI-repo](https://github.com/theafh/ai-modules).

## Domain

Agentic AI for chip design. The wiki holds three kinds of content. Reference pages summarize external
literature and external open-source projects. Incident pages record defects, limits and decisions in
this project. Procedure pages record how to act in this project.

## Conventions

- **Folder layout is the type axis only, with two deliberate exceptions.** Most pages live directly at
  `<pluralized-type>/<slug>.md`, flat, one layer deep (`raw/papers/03-rtl.md`,
  `incidents/001-np-diag-returns-1d.md`). No thematic prefix folders, no sub-folders inside a type
  folder, no pages at the wiki root. Thematic scope is expressed through `tags:` and `type:`, both of
  which have explicit declared sets in this schema. The folder tree does not carry a second axis.
  **Type names are singular, folder names are plural: the linter derives the folder from the type by
  pluralizing.**
  The two exceptions are the `tasks/` area, described below, and `raw/papers/`, where the generated
  paper pages live beside the raw paper PDFs (decided 2026-10-17; the generated pages stay inside
  the wiki tree but out of the type axis).
- File names: lowercase, hyphens, no spaces.
- Every wiki page starts with YAML frontmatter, described below.
- Cross-link with standard relative markdown links: `[index](../index.md)` from a type folder, and
  `[RTL](03-rtl.md)` from the same folder. Every page needs a minimum of 2 outbound links.
- When updating a page, bump the `updated` date.
- Every page must appear in `index.md`.
- Every action must be appended to `log.md`.
- **Provenance:** attribution belongs next to the claim it attributes. A reference page cites each
  paper or project with an inline link in the table row that names it. Pages carry no body "Sources"
  section and no footnote markers.

## Generated and hand-written pages

This is the rule that matters most here, because the wiki holds both kinds.

Every page under `raw/papers/` is **generated**. `tools/build_wiki.py` writes the nine AI4CHIPS section
pages and `tools/ingest_neuromorphic.py` writes the Open Neuromorphic pages. Do not hand-edit a
generated page, and do not split one. The next build overwrites the edit, or the split desyncs from the
generator and nobody notices.

Three parts of a generated page are model-written and preserved across a rebuild: the "What this
covers" section, the "Themes" section and the "Notable entries" section. Everything else, including
the frontmatter, the paper table and the summaries, is regenerated from the source index each run.

To change the shape of a generated page, change the generator and rebuild. A repair tool that edits
these pages in place is the wrong instrument, however correct its findings are.

Pages under `incidents/` and `procedures/` are hand-written and have no generator.

## The tasks area

Most pages live at `<pluralized-type>/<slug>.md` flat, one layer deep, as stated above. References, incidents and procedures follow that rule. The `tasks/` area is the one deliberate exception. It groups working records by activity rather than by type. It holds two sub-areas: `tasks/musings/` for dated deliberation records and `tasks/hypothesis/` for investigation records.

A page inside `tasks/` still declares its `type` in frontmatter. The folder does not carry the type there. A page in `tasks/musings/` declares `type: musing` and a page in `tasks/hypothesis/` declares `type: task`. The linter flags every page under `tasks/` as misfiled at blocking severity. Its rule derives the folder from the type and permits no sub-folder. That finding is expected and accepted. Nobody should flatten `tasks/` to silence it.

A relative link from a page in a sub-area to the wiki index is `../../index.md`. That is two levels up, not one.

## Frontmatter

```yaml
title: Page Title
created: YYYY-MM-DD
updated: YYYY-MM-DD
type: incident | procedure | reference | bug | test | solution | concept | entity | comparison | query | summary | musing | task
tags: [from taxonomy below]
sources: []
status: open | closed
```

`sources:` is the canonical inventory of raw files captured **under the wiki root**. The linter
validates each entry against the `raw/<kind>/<slug>.md` path pattern. Every page today carries
`sources: []` because no page yet cites a capture file. Reference pages cite external arXiv URLs or
project pages inline per row, and incident pages cite commit hashes and source paths in the body.
When a page draws on captured material, list it in `sources:`. Large fetched material lives outside
git: fetched paper PDFs sit under `raw/papers/` inside the wiki tree (git-ignored by path), and the
cloned source repos sit at the repo root under `raw/pdf/` and `raw/git/`.

## Tag Taxonomy

- Kind: bug, reference, procedure
- Design stage: rtl, hls, netlist, layout, architecture, analog, verification, security
- Domain: neuromorphic, snn, eda, benchmark
- Components: photonic, testbench, flow
- Techniques: numpy, cocotb, orfs, makefile, docker, yosys
- Meta: regression-test, generated

Rule: every tag on a page must appear in this taxonomy. To use a new tag, add it here first.

## Page Types

| Type | Purpose |
| --- | --- |
| reference | A summary of external literature or external projects, generated from a source index |
| incident | A defect, limit or decision with symptom, root cause, fix and regression test |
| procedure | A rule or workflow for how to act in this project |
| bug | A defect with no fix yet, or a fix linked to many pages |
| test | A test that covers multiple pages, or a test unlinked to one defect |
| solution | A reusable remedy that applies across two or more defects |
| entity | A named person, organization, product, model, or place |
| concept | An idea or mechanism, what it means and why |
| comparison | Two items compared side by side with a verdict |
| query | An answer to one specific question, question-organized |
| summary | An overview or topic-organized digest |
| musing | A dated, immutable record of a decision or a deliberation at one point in time |
| task | An investigation record that stays open while evidence arrives and freezes when closed |

## Reference Pages

Answers "what exists in the literature on this topic?" One page per section of a source index.
Generated. Sections in this order:

- What this covers: the scope of the section, model-written and preserved across a rebuild
- Themes: the sub-themes observed in the data, model-written and preserved
- Papers: the full table, regenerated every run
- Notable entries: model-written and preserved
- Paper summaries: one entry per paper that has an abstract, regenerated when asked

## Incident Pages

Answers "what happened, why, and how was it fixed?" One page per defect, limit or decision. Sections
in this order:

- Symptom: what a person sees when the fault happens, with the exact error text
- Root cause: why the fault happens, with the file name and the line number
- Fix: what changed and where
- Regression test: the test that fails if the fault returns, and whether somebody confirmed that it
  fails on the old code
- Notes: optional

## Bug Pages

A defect page when the defect has no fix yet, or when one fix spans many pages. One page per defect.
Sections in this order:

- Symptom: what a person sees when the fault happens, with the exact error text
- Root cause: why the fault happens, with the file name and the line number
- Workaround: optional steps to reduce the impact
- See also: links to other pages affected by this defect
- Notes: optional

## Test Pages

A test page when a test covers many pages, or when it is not linked to one defect. One page per test.
Sections in this order:

- Purpose: what this test verifies
- Coverage: which pages or systems this test exercises
- Trigger: how to run the test
- Expected result: what success looks like
- Notes: optional

## Solution Pages

A reusable remedy that applies across two or more defects. One page per solution. Sections in this order:

- Rule: the remedy stated as a principle or practice
- When to apply: the conditions that trigger this remedy
- Incidents fixed: links to every incident page this solution addresses
- Notes: optional

## Choosing a page type

An incident page holds symptom, root cause, fix and regression test as one story. Use an incident
page when one defect has one fix and one test. Use a bug page when the defect has no fix yet or when
one fix spans many pages. Use a test page when the test covers many pages or when it is unlinked to
one defect. Use a solution page when one remedy already applies to two or more defects and you want
one place to state it. A solution page links to every incident page it covers, which satisfies the
outbound-link minimum. Use a musing page when you want a dated, immutable record of a decision or a deliberation at this moment. Use a task page to record a failure under investigation while evidence arrives and to preserve killed hypotheses after the investigation closes.

## Procedure Pages

Answers "how should this be done?" One page per rule or workflow. Sections in this order:

- A one-paragraph summary that states the rule and its scope
- When this applies: the trigger
- The rule, or the steps
- Pitfalls: optional
- See also: links to related pages

## Musing Pages

A dated, immutable record of a decision or a deliberation. One page per decision. Sections in this order:

- Verdict: one or two sentences, stated flatly
- Argument: why the verdict holds
- Rejection rationale: what the author considered and declined, and on what grounds
- Related: links to incidents, to backlog entries and to other musings

### Immutability Rule

A musing is immutable after the day somebody writes it. The `updated` date always equals the `created` date. To revise a verdict, add a new dated musing and link it to the one it supersedes. The superseded musing gains one line at its top naming its successor. That line is the only permitted content edit. A typo fix or a broken-link fix is permitted and does not bump `updated`. A musing records what somebody believed at a moment. An edit that rewrites an old verdict destroys the record.

### Choosing between musing, comparison and concept

A musing is dated, immutable, a decision or deliberation at a point in time. A comparison is living, revised as the answer changes, a maintained structured weighing. A concept is living, explains a thing rather than deciding anything. A musing must never be converted into a comparison. A maintained position page is a new comparison page that cites the musings as its history.

## Task Pages

An investigation record that stays open while evidence arrives and freezes when the investigation closes. One page per investigation. Sections in this order:

- A one-line statement of the failure under investigation
- Ranked hypotheses, each with its evidence for, its evidence against, and its verdict
- Related: links to incidents and other task pages

While `status: open`, the page is a living document. Bump `updated` on every edit. Kill a hypothesis in place and record what killed it. Add evidence as it arrives. When the investigation closes, set `status: closed` and add a `closed: YYYY-MM-DD` field. From that date the page is immutable, exactly like a musing, except that link edits stay permitted.

A confirmed hypothesis graduates to an incident page, and the task page links to it. A killed hypothesis stays on the task page with its kill evidence and never gets its own page. The killed hypotheses are the main value of a closed task page, because they record proven dead ends.

### Killed vs. absence of evidence

A hypothesis is killed only by disproof. Somebody reads a file or runs a check. The evidence contradicts the hypothesis. A failure that stops reproducing gives no disproof. It gives absence of evidence. These two verdicts are different.

Record a non-reproducing failure as an evidence line. Name the run and the conditions. Do not mark any hypothesis killed because of absence. A set whose failure stopped reproducing stays `status: open`. The investigation has no answer yet.

Set `status: closed` only when the investigation reached an answer. One hypothesis is confirmed. Or every hypothesis is killed by disproof. A non-reproducing failure looks exactly like a fix. A page closed on that basis loses the ability to recognize the failure when it returns.

## Linter Notes

The linter is `scripts/lint.py` in the `knowledge_management` plugin. Run it with the wiki directory
as the positional argument. It reports and it changes nothing.

Four constraints are easy to break by habit:

- Do not put a horizontal rule in the body of a page. The linter reads a line of three dashes as a
  list marker with no space after it.
- Give every fenced code block a language identifier. Use `shell` for a command, `python` for Python
  code or a Python error, and `text` for the output of another tool.
- Give every page a minimum of 2 outbound links, and list every page in `index.md`. A page with no
  inbound link is an orphan and the linter warns.
- Keep `sources:` empty here, for the reason given above.

This wiki holds zero em dashes and zero en dashes. That is a project rule and not a linter rule, so
the linter does not check it. Check it by codepoint, because an editor and a language model both
insert one silently.

### Accepted findings

`raw/papers/03-rtl.md` holds 97 papers in one table and passes 200 lines. The linter reports an
oversized page at info level. The rationale is that the page boundary follows the source index
section, which is the unit a reader navigates by, and a split would desync from the generator. The
finding is accepted and not fixed.

Types `solution`, `concept`, `entity`, `comparison`, `query` and `summary` are declared in the enum
and their folders exist with `.gitkeep` files, but no page uses them yet. The linter may report
them as unused at info level. This is deliberate: types are declared ahead of use so the linter does
not warn when the first page of each type is created.

Every page under `tasks/` is reported as misfiled at blocking severity because the linter derives the folder from the type and permits no sub-folder. That finding is expected and accepted. The user requires the nested layout; the linter cannot express it. Nobody should flatten `tasks/` to silence the linter.

If a stale finding ever appears on a musing page, it is accepted. The immutability rule is the rationale: `updated` never changes after the day a musing is written.

The linter expects a top-level `musings/` folder because `musing` is declared in the page-type enum. Musing pages live at `tasks/musings/` by direction. Creating an empty `musings/` folder at the wiki root would mislead every future reader about where to find musings. The warning is accepted. Do not create the empty folder.

## Update Policy

When new information conflicts with existing content:

1. Check the dates. A newer source usually supersedes an older one.
2. If the conflict is genuine, record both positions with their dates and their sources.
3. Bump the `updated` date.

[Wiki index](index.md)
