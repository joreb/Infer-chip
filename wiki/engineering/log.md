# Wiki Log

> Chronological record of all wiki actions. Append-only.
> Format: `## [YYYY-MM-DD] action | subject`
> Actions: ingest, update, query, lint, create, archive, delete
> Body: list only files actually created or updated. Skip files that were
> inspected, considered, or deliberately left unchanged, and do not narrate
> decisions about what not to do. Aim for roughly 20 lines per entry.
> When this file exceeds 500 entries, rotate: rename to log-YYYY.md, start fresh.

## [2026-10-17] restructure | Conform to knowledge_management schema

- Created SCHEMA.md with domain scope, conventions, and tag taxonomy
- Created index.md with entry list for all pages
- Created procedures/add-an-engineering-log-entry.md with workflow steps and field definitions
- Moved 001-np-diag-returns-1d.md to incidents/001-np-diag-returns-1d.md with YAML frontmatter
- Moved 002-cocotb-check-results-module.md to incidents/002-cocotb-check-results-module.md with YAML frontmatter
- Moved 003-tail-without-pipefail.md to incidents/003-tail-without-pipefail.md with YAML frontmatter
- Moved 004-tb-range-pad-non-pow2.md to incidents/004-tb-range-pad-non-pow2.md with YAML frontmatter
- Moved 005-orfs-make-run-is-per-stage-noop.md to incidents/005-orfs-make-run-is-per-stage-noop.md with YAML frontmatter
- Removed README.md and _template.md (content consolidated into index.md and procedures/)
- Added cross-links between all pages to satisfy minimum link requirements
