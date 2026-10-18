# Wiki Log

> Chronological record of all wiki actions. Append-only.
> Format: `## [YYYY-MM-DD] action | subject`
> Actions: ingest, update, query, lint, create, archive, delete
> Body: list only files actually created or updated. Skip files that were
> inspected, considered, or deliberately left unchanged, and do not narrate
> decisions about what not to do. Aim for roughly 20 lines per entry.
> When this file exceeds 500 entries, rotate: rename to log-YYYY.md, start fresh.

## [2026-10-17] migrate and create | Musing pages from tasks to wiki

- Moved 4 musing pages from tasks/musings/ to wiki/musings/ using git mv
- Added YAML frontmatter to each musing with created/updated dates and tags
- Replaced Related sections with intra-wiki links to musings and wiki index
- Created 1 new musing: SpikeLLM is not a target for the fabric
- Added Musings section to wiki/index.md with all five pages and one-line verdicts
- Cross-linked musings and verified all five pages exist under wiki/musings/

## [2026-10-17] restructure | Wiki schema conformance

- Created `wiki/references/` directory for generated reference pages
- Created `wiki/incidents/` directory and moved 7 incident pages from wiki/engineering/incidents/
- Created `wiki/procedures/` directory and moved 1 procedure page from wiki/engineering/procedures/
- Deleted `wiki/engineering/` tree and its nested schema, index, and log files
- Created root `wiki/index.md` with markers for generated content and listings of incidents and procedures
- Created root `wiki/log.md` with preamble and initial restructure entry
- Edited `tools/build_wiki.py` to write to `wiki/references/<slug>.md` with YAML frontmatter, updated `wiki/index.md` with markers, and append to `wiki/log.md`
- Edited `tools/ingest_neuromorphic.py` to write to `wiki/references/onm-<slug>.md` with YAML frontmatter, update `wiki/index.md` with markers, and append to `wiki/log.md`
- Verified both generator selftests pass

## [2026-10-17] update | AI4CHIPS reference pages

- Rebuilt 9 reference pages under references/

## [2026-10-17] update | AI4CHIPS reference pages

- Rebuilt 9 reference pages under references/

## [2026-10-17] update | AI4CHIPS reference pages

- Rebuilt 9 reference pages under references/

## [2026-10-17] update | Open Neuromorphic reference pages

- Rebuilt 5 reference pages under references/

## [2026-10-17] update | Open Neuromorphic reference pages

- Rebuilt 5 reference pages under references/

## [2026-10-17] update | AI4CHIPS reference pages

- Rebuilt 9 reference pages under references/

## [2026-10-17] update | Open Neuromorphic reference pages

- Rebuilt 5 reference pages under references/

## [2026-10-17] update | AI4CHIPS reference pages

- Rebuilt 9 reference pages under references/

## [2026-10-17] update | AI4CHIPS reference pages

- Rebuilt 9 reference pages under references/

## [2026-10-17] restructure | Tasks area official in schema and index

- Updated SCHEMA.md conventions bullet to state that tasks/ is the one deliberate exception to flat layout
- Added new section "The tasks area" to SCHEMA.md documenting nested structure and link depths
- Added task type to frontmatter enum in SCHEMA.md and Page Types table
- Added status field (open/closed) to frontmatter specification
- Added Task Pages section to SCHEMA.md with anatomy, update rule, and graduation rules for hypotheses
- Added guidance for task pages to "Choosing a page type" section
- Added accepted findings entry for structure warnings on pages under tasks/
- Fixed 5 broken links in tasks/musings/ pages: changed ../index.md to ../../index.md
- Added frontmatter to tasks/hypothesis/2026-10-17-1-synth-load-design-fail.md with type: task, status: open, tags: [flow, orfs, yosys]
- Moved Musings section in index.md into new Tasks section with two subsections
- Updated all musing links in index.md from musings/ to tasks/musings/
- Added Hypotheses subsection to Tasks section in index.md with the one open investigation
- Deleted tasks/musings/README.md and tasks/hypothesis/README.md (content folded into index.md)

## [2026-10-17] create | First bug page

- Created bugs/orchestrator-run-dir-has-no-lock.md with symptom, root cause, workaround, proposed fix, and notes
- Added Bugs section to wiki/index.md listing the new page
- Added inbound link from incidents/003-tail-without-pipefail.md to the bug page in See also section

## [2026-10-17] update | AI4CHIPS reference pages

- Rebuilt 9 reference pages under references/

## [2026-10-17] audit | 0 blocking, 0 warn, 0 info; 4 pages updated, 0 pages split

- Lint: 7 blocking tasks/ misfiled findings, 1 musings/ missing-folder warn and 3 info findings remain, all pre-accepted in SCHEMA.md "Accepted findings"; no new blocking or warn finding introduced
- Ran the full audit walk over incidents/001-007, bugs/orchestrator-run-dir-has-no-lock.md, procedures/add-an-engineering-log-entry.md, all 6 musings and the open hypothesis task page; check broken links (all resolve), index completeness (every page listed exactly once), page anatomy and the zero-dash project rule
- tasks/hypothesis/2026-10-17-1-synth-load-design-fail.md: stripped 5 em dashes (project rule) and converted the Related section's plaintext wiki paths to real relative markdown links, satisfying the 2-outbound-link minimum
- tasks/musings/2026-10-17-riscv-is-control-plane-not-the-fabric.md: stripped 4 em dashes; verified musing-type rules hold (dated, immutable, verdict section present, links resolve)
- tasks/musings/2026-10-17-llms-on-snn-hardware.md: added a Related link to the RISC-V control-plane musing, clearing its only-inbound orphan warn; link-only edit, no verdict rewritten
- tasks/musings/2026-10-17-spikellm-is-not-a-target-for-the-fabric.md: corrected the BindSNET Related link label to the target page's real title
- Verified the new riscv musing's index entry links to the real file and matches its summary
## [2026-10-17] update | Generated paper pages stay in wiki after layout decision

- User decision 2026-10-17: the proposal to move the generated pages from wiki/references/ to docs/papers/ is rejected. wiki/ holds both hand-written and generated pages.
- The tools/build_wiki.py and tools/ingest_neuromorphic.py output paths and wiki/index.md are unchanged as part of the decision; a migration was started and reverted the same day with no commit.
- The tasks/ nested layout and the SCHEMA.md accepted-findings list are unchanged.

## [2026-10-17] update | AI4CHIPS reference pages

- Rebuilt 9 reference pages under raw/papers/

## [2026-10-17] update | Open Neuromorphic reference pages

- Rebuilt 5 reference pages under raw/papers/
## [2026-10-17] migrate | Generated paper pages from references/ to raw/papers/

- Moved 14 generated pages from wiki/references/ to wiki/raw/papers/ with git mv, beside the fetched paper PDFs already under wiki/raw/papers/.
- tools/build_wiki.py and tools/ingest_neuromorphic.py write to wiki/raw/papers/ and their wiki/index.md table links point at raw/papers/. Generated page footers now link the index at ../../index.md.
- wiki/index.md hand-written prose links updated to raw/papers/.
- wiki/SCHEMA.md: layout rule now states two deliberate exceptions, tasks/ and raw/papers/.
- The spikellm musing mentions the new path.
- Both generator selftests pass; a full offline rebuild ran clean from the new location.
## [2026-10-18] update | Incidents ENG-009 and ENG-010, bugs page rewritten as a beginner tutorial

- New incidents/009-copy-out-path-and-no-metadata.md: GitHub #1. The cd flow in the container script broke the copy paths, and bare make never writes metadata.json. Fix dfef3b6, also docker_cmd.txt, named container killed on timeout, 7200 s timeout. Proof: orchestrated 128-neuron run inv f6599c24.
- New incidents/010-parse-metrics-took-cts-stage-values.md: parse_metrics took the first stage key (cts__). Fix f6d6b51 names finish__ and detailedroute__ keys first; real-metadata fixture test confirmed to fail on the old code.
- bugs/orchestrator-run-dir-has-no-lock.md: rewritten as a tutorial for chip-design beginners, marked fixed (a8241a1, GitHub #8), regression test named.
- SCHEMA.md: optional "Background for beginners" section for incident and bug pages.
- ENG-008 stays reserved for the SDC braces page (GitHub #3).
- In progress, no page yet: dense-ROM baseline (GitHub #2, commit 175c76c). The comparison page comes when the 128-neuron ROM run has numbers.
## [2026-10-18] update | Research summaries and the ROM baseline comparison

- New summaries/fractal-and-hierarchical-neuromorphic-designs.md: digest of a research-agent literature scan (Braindrop H-tree, DYNAPs, Mosaic, Rent's rule, mesh chips, gaps, 3 experiments).
- New summaries/cmos-compute-in-memory.md: digest of a research-agent literature scan (digital and analog SRAM CIM, SNN CIM, ORRAM, OpenRAM, Ankhdjet, limits, 3 experiments).
- New comparisons/rom-vs-external-sram-weights.md: GitHub #2 result, 128 neurons, runs f6599c24 and 15914a90.
- Downloaded the 29 cited arXiv PDFs to raw/papers/<id>.pdf (git-ignored); page-1 titles of the 2026 ids match the summaries.
- index.md: new Summaries and Comparisons sections.
## [2026-10-18] update | Weight storage hierarchy concept page

- New concepts/weight-storage-hierarchy.md: SSD, DDR5, HBM and on-chip memory against the needs of the core (512-bit word per cycle, fixed 1-cycle latency); load-then-run path over SPI (GitHub #11); double-buffered streaming; scale check for 1 Tb and 1 T-parameter models (about 95 sky130 wafers of OpenRAM per Tb).
- index.md: new Concepts section.
## [2026-10-18] update | Tutorials and glossary

- New tutorials/ type folder with 4 numbered tutorials for chip-design newcomers: the spiking neuron core, Verilog to GDS, reading PPA metrics, running the agent loop. Each has real commands and values from this project and check questions.
- New concepts/glossary.md: key terms in alphabetical order, each defined for this project.
- SCHEMA.md: new page type `tutorial` with its section anatomy.
- index.md: new Tutorials section; glossary under Concepts.
