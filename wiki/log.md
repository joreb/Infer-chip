# Wiki Log

> Chronological record of all wiki actions. Append-only.
> Format: `## [YYYY-MM-DD] action | subject`
> Actions: ingest, update, query, lint, create, archive, delete
> Body: list only files actually created or updated. Skip files that were
> inspected, considered, or deliberately left unchanged, and do not narrate
> decisions about what not to do. Aim for roughly 20 lines per entry.
> When this file exceeds 500 entries, rotate: rename to log-YYYY.md, start fresh.

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
