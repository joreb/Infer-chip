#!/usr/bin/env python3
"""Build the AI4CHIPS wiki from the upstream paper index.

Pulls the source README from GitHub, parses every section table, fetches arXiv
metadata for every arXiv paper in one batched API pass, and writes one wiki page
per section.

Model-written prose is preserved. The script regenerates only the mechanical
parts of each page: the title, the blockquote, the paper table and (with
--rebuild-summaries) the summary list. Sections listed in PRESERVED are copied
from the existing page untouched, so a rebuild never destroys hand-written or
agent-written prose.

Usage:
    python tools/build_wiki.py                     # build, keep existing prose
    python tools/build_wiki.py --rebuild-summaries # also regenerate summaries
    python tools/build_wiki.py --offline           # use cached downloads only
    python tools/build_wiki.py --selftest          # run parser checks, no I/O
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

SOURCE_URL = "https://raw.githubusercontent.com/Archerll/AI4CHIPSpaper/main/README.md"
SOURCE_REPO = "https://github.com/Archerll/AI4CHIPSpaper"
ARXIV_API = "http://export.arxiv.org/api/query"
ARXIV_BATCH = 50
ARXIV_DELAY_S = 3.5

ROOT = Path(__file__).resolve().parent.parent
WIKI_DIR = ROOT / "wiki"
# Generated paper pages live under wiki/raw/papers (since 2026-10-17):
# user decision — the raw-source derived pages sit beside the raw paper
# PDFs under wiki/raw/, inside the wiki tree.
REFERENCES_DIR = WIKI_DIR / "raw" / "papers"
CACHE_DIR = Path(__file__).resolve().parent / ".cache"

OLLAMA_URL = "http://localhost:11434"
# deepseek-v4-flash was retired on 2026-09-25. deepseek-v4-pro:cloud is the
# working DeepSeek tier; glm-5.3-flash:cloud is the fast substitute.
OLLAMA_MODEL = "deepseek-v4-pro:cloud"
OLLAMA_TIMEOUT_S = 120
OLLAMA_RETRIES = 2

STE_PROMPT = """Write a summary of one hardware-design paper for a technical wiki.

Rules for the summary:
- Write one or two sentences. Use a maximum of 20 words per sentence.
- Use ASD-STE100 Simplified Technical English.
- Use the active voice and the simple present tense.
- State the problem the paper addresses and the method it uses.
- Give a number only if the abstract gives that number.
- Add no claim that the abstract does not make. Add no opinion about quality.
- Use no em dash, no en dash, no semicolon and no parentheses.
- Do not repeat the title. Do not write a preamble. Output the sentences only.

Title: {title}

Abstract: {abstract}

Summary:"""

# Headings whose body is written by a model and must survive a rebuild.
PRESERVED = ("What this covers", "Themes", "Notable entries", "Paper summaries")

# Section-name overrides for the page title. Anything absent keeps its own name.
TITLE_OVERRIDES = {
    "HLS": "HLS (High-Level Synthesis)",
    "RTL": "RTL (Register Transfer Level)",
}

EMPTY_CELL = "n/a"
SECTION_RE = re.compile(
    r"<details><summary><h2[^>]*>(?P<name>.*?)</h2></summary>(?P<body>.*?)</details>",
    re.S,
)
BADGE_RE = re.compile(r"!\[[^\]]*\]\([^)]*\)")
ARXIV_ID_RE = re.compile(r"arxiv\.org/(?:abs|pdf)/(\d{4}\.\d{4,5})")
EMPTY_LINK_RE = re.compile(r"\[\s*\]\((?P<url>[^)]+)\)")
DASHES = {"—": ". ", "–": " to "}


# --------------------------------------------------------------------------- #
# parsing
# --------------------------------------------------------------------------- #
def slugify(name: str) -> str:
    s = name.strip().rstrip(".").lower().replace("&", "and")
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-")


def scrub_dashes(text: str) -> str:
    """Remove em and en dashes from generated text.

    ASD-STE100 output carries no dashes as punctuation. Applied to generated
    cells only, never to preserved prose, because a blanket substitution inside
    a sentence produces nonsense.
    """
    for bad, good in DASHES.items():
        text = text.replace(bad, good)
    return re.sub(r"\s{2,}", " ", text).strip()


def clean_cell(cell: str) -> str:
    cell = BADGE_RE.sub("", cell).strip()
    return scrub_dashes(cell) or EMPTY_CELL


def parse_rows(body: str) -> list[dict]:
    """Parse one section body into paper rows.

    Source row layout: Date|Method|Type|Conference|Title|Code. The Type column
    only holds shield badges, so it is dropped. maxsplit keeps any stray pipe in
    the Code cell instead of losing the field.
    """
    rows = []
    for line in body.splitlines():
        line = line.strip()
        if not line or "|" not in line:
            continue
        if line.startswith("Date|") or set(line) <= set("-|"):
            continue
        parts = line.split("|", 5)
        if len(parts) < 5:
            continue
        parts += [""] * (6 - len(parts))
        date, method, _type, venue, title, code = parts
        method = EMPTY_LINK_RE.sub(r"[paper](\g<url>)", method.strip())
        rows.append(
            {
                "date": clean_cell(date),
                "name": clean_cell(method),
                "venue": clean_cell(venue),
                "title": clean_cell(title),
                "code": clean_cell(code),
                "arxiv": sorted(set(ARXIV_ID_RE.findall(f"{method} {title} {code}"))),
            }
        )
    return rows


def parse_sections(readme: str) -> list[dict]:
    sections = []
    for i, m in enumerate(SECTION_RE.finditer(readme), start=1):
        name = m.group("name").strip().rstrip(".")
        rows = parse_rows(m.group("body"))
        sections.append(
            {
                "index": i,
                "name": name,
                "title": TITLE_OVERRIDES.get(name, name),
                "slug": f"{i:02d}-{slugify(name)}",
                "rows": rows,
            }
        )
    if not sections:
        raise SystemExit("no <details> sections found: upstream layout changed")
    return sections


# --------------------------------------------------------------------------- #
# fetching
# --------------------------------------------------------------------------- #
def fetch(url: str, cache_name: str, offline: bool) -> str:
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    cached = CACHE_DIR / cache_name
    if offline:
        if not cached.exists():
            raise SystemExit(f"--offline but no cache at {cached}")
        return cached.read_text(encoding="utf-8")
    with urllib.request.urlopen(url, timeout=60) as r:
        text = r.read().decode("utf-8")
    cached.write_text(text, encoding="utf-8")
    return text


def fetch_arxiv(ids: list[str], offline: bool) -> dict[str, dict]:
    """Return {arxiv_id: {title, abstract}} using the batched arXiv API.

    One request per 50 ids, not one per paper. Results are cached, so a rebuild
    only requests ids the cache does not already hold.
    """
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    cached_path = CACHE_DIR / "arxiv.json"
    meta: dict[str, dict] = {}
    if cached_path.exists():
        meta = json.loads(cached_path.read_text(encoding="utf-8"))

    missing = [i for i in ids if i not in meta]
    if missing and offline:
        print(f"  offline: {len(missing)} ids have no cached metadata", file=sys.stderr)
        return meta

    ns = {"a": "http://www.w3.org/2005/Atom"}
    for start in range(0, len(missing), ARXIV_BATCH):
        batch = missing[start : start + ARXIV_BATCH]
        url = f"{ARXIV_API}?id_list={','.join(batch)}&max_results={len(batch)}"
        try:
            with urllib.request.urlopen(url, timeout=90) as r:
                xml = r.read()
        except urllib.error.URLError as exc:
            print(f"  arXiv batch at {start} failed: {exc}", file=sys.stderr)
            continue
        for entry in ET.fromstring(xml).findall("a:entry", ns):
            raw_id = (entry.findtext("a:id", default="", namespaces=ns) or "").strip()
            aid = re.sub(r"v\d+$", "", raw_id.rsplit("/", 1)[-1])
            meta[aid] = {
                "title": " ".join(
                    (entry.findtext("a:title", default="", namespaces=ns) or "").split()
                ),
                "abstract": " ".join(
                    (entry.findtext("a:summary", default="", namespaces=ns) or "").split()
                ),
            }
        print(f"  arXiv {min(start + ARXIV_BATCH, len(missing))}/{len(missing)}")
        if start + ARXIV_BATCH < len(missing):
            time.sleep(ARXIV_DELAY_S)

    cached_path.write_text(json.dumps(meta, indent=1, sort_keys=True), encoding="utf-8")
    return meta


# --------------------------------------------------------------------------- #
# rendering
# --------------------------------------------------------------------------- #
def split_existing(path: Path) -> dict[str, str]:
    """Map heading text to its body for an existing page.

    Reads pages with YAML frontmatter by skipping the frontmatter block.
    Strips trailing footer artifacts: blank lines, trailing horizontal rules,
    and trailing markdown link lines.
    """
    if not path.exists():
        return {}
    blocks: dict[str, str] = {}
    heading = None
    buf: list[str] = []
    lines = path.read_text(encoding="utf-8").splitlines()

    # Skip YAML frontmatter if present
    start_idx = 0
    if lines and lines[0] == "---":
        for i in range(1, len(lines)):
            if lines[i] == "---":
                start_idx = i + 1
                break

    for line in lines[start_idx:]:
        if line.startswith("## "):
            if heading:
                blocks[heading] = _strip_trailing_footer("\n".join(buf).strip("\n"))
            heading = line[3:].strip()
            buf = []
        elif heading:
            buf.append(line)
    if heading:
        blocks[heading] = _strip_trailing_footer("\n".join(buf).strip("\n"))
    return blocks


def _strip_trailing_footer(text: str) -> str:
    """Remove trailing footer artifacts from captured block text.

    Strips trailing blank lines, trailing horizontal rule (---), and
    trailing markdown link lines to clean up stale footers. Loops until
    nothing more matches to handle artifacts stacked in any order.
    """
    lines = text.split("\n")

    # Loop until nothing more changes
    while True:
        initial_len = len(lines)

        # Drop trailing blank lines
        while lines and not lines[-1].strip():
            lines.pop()

        # Drop trailing horizontal rule (exactly three or more dashes)
        if lines and re.match(r"^-{3,}$", lines[-1].strip()):
            lines.pop()

        # Drop trailing markdown link line (e.g., "[text](url)" or "- [text](url)")
        if lines and re.match(r"^(?:-\s*)?\[.+\]\(.+\)\s*$", lines[-1].strip()):
            lines.pop()

        # If nothing changed this iteration, we're done
        if len(lines) == initial_len:
            break

    return "\n".join(lines)


def first_sentences(abstract: str, limit: int = 2) -> str:
    """Take the opening sentences of an abstract as a factual summary."""
    parts = re.split(r"(?<=[.!?])\s+(?=[A-Z(])", abstract)
    text = " ".join(parts[:limit]).strip()
    return scrub_dashes(text)


class Summarizer:
    """Turns an abstract into a wiki summary.

    With no model it takes the opening sentences of the abstract. With a model
    it asks Ollama for an ASD-STE100 summary. Every answer is cached by model
    and arXiv id, so an interrupted run resumes without paying again.
    """

    def __init__(self, model: str | None, url: str = OLLAMA_URL):
        self.model = model
        self.url = url.rstrip("/")
        self.path = CACHE_DIR / "summaries.json"
        self.cache: dict[str, str] = {}
        if self.path.exists():
            self.cache = json.loads(self.path.read_text(encoding="utf-8"))
        self.calls = 0
        self.failures = 0

    def _ask(self, title: str, abstract: str) -> str | None:
        payload = json.dumps(
            {
                "model": self.model,
                "prompt": STE_PROMPT.format(title=title, abstract=abstract),
                "stream": False,
                "options": {"temperature": 0.2},
            }
        ).encode("utf-8")
        req = urllib.request.Request(
            f"{self.url}/api/generate",
            data=payload,
            headers={"Content-Type": "application/json"},
        )
        for attempt in range(OLLAMA_RETRIES + 1):
            try:
                with urllib.request.urlopen(req, timeout=OLLAMA_TIMEOUT_S) as r:
                    answer = json.loads(r.read().decode("utf-8")).get("response", "")
                return " ".join(answer.split()) or None
            except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
                if attempt == OLLAMA_RETRIES:
                    print(f"    ollama failed: {exc}", file=sys.stderr)
                    return None
                time.sleep(2 * (attempt + 1))
        return None

    def summarize(self, aid: str, entry: dict) -> str:
        fallback = first_sentences(entry["abstract"])
        if not self.model:
            return fallback
        key = f"{self.model}|{aid}"
        if key in self.cache:
            return self.cache[key]
        answer = self._ask(entry["title"], entry["abstract"])
        self.calls += 1
        if not answer:
            self.failures += 1
            return fallback
        text = scrub_dashes(answer).strip().strip('"')
        if len(text) < 20:  # model refused or returned a stub
            self.failures += 1
            return fallback
        self.cache[key] = text
        return text

    def save(self) -> None:
        """Merge into the cache file rather than overwrite it.

        build_wiki.py and ingest_neuromorphic.py share this file and can run at
        the same time. A plain write would drop whichever run finished first.
        """
        if not self.cache:
            return
        CACHE_DIR.mkdir(parents=True, exist_ok=True)
        merged = {}
        if self.path.exists():
            try:
                merged = json.loads(self.path.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                merged = {}
        merged.update(self.cache)
        self.path.write_text(
            json.dumps(merged, indent=1, sort_keys=True), encoding="utf-8"
        )


def render_summaries(
    rows: list[dict], meta: dict[str, dict], summarizer: Summarizer
) -> str:
    lines = [
        "Each summary below comes from the abstract of the paper on arXiv. "
        "Papers that are not on arXiv have no summary here.",
        "",
    ]
    for row in rows:
        for aid in row["arxiv"]:
            if aid not in meta:
                continue
            label = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", row["name"])
            if label == EMPTY_CELL:
                label = row["title"][:60]
            summary = summarizer.summarize(aid, meta[aid])
            lines.append(
                f"- **{label}** ([arXiv:{aid}](https://arxiv.org/abs/{aid})). {summary}"
            )
    return "\n".join(lines)


def render_page(
    section: dict,
    meta: dict[str, dict],
    largest: str,
    rebuild: bool,
    summarizer: Summarizer,
) -> str:
    rows = section["rows"]
    existing = split_existing(REFERENCES_DIR / f"{section['slug']}.md")

    # Map section number to topic tags from taxonomy
    # Slug format is always "NN-name", extract the number
    slug_num_match = re.match(r"(\d+)", section["slug"])
    section_num = int(slug_num_match.group(1)) if slug_num_match else 1
    topic_tags = {
        1: "benchmark",
        2: "hls",
        3: "rtl",
        4: "verification",
        5: "security",
        6: "architecture",
        7: "netlist",
        8: "layout",
        9: "analog",
    }
    topic_tag = topic_tags.get(section_num, "reference")

    note = (
        " It is the largest section of the index."
        if section["slug"] == largest
        else ""
    )

    # Determine the previous and next section slugs for See also links
    # (will be filled in during the main function)
    prev_slug = section.get("_prev_slug")
    prev_title = section.get("_prev_title")
    next_slug = section.get("_next_slug")
    next_title = section.get("_next_title")

    frontmatter = [
        "---",
        f"title: {section['title']}",
        "created: 2026-10-17",
        "updated: 2026-10-17",
        "type: reference",
        f"tags: [reference, generated, {topic_tag}]",
        "sources: []",
        "---",
        "",
    ]

    out = frontmatter + [
        f"# {section['title']}",
        "",
        f"> Section of the [AI4CHIPS paper index]({SOURCE_REPO}). "
        f"{len(rows)} papers.{note}",
        "",
    ]

    for heading in ("What this covers", "Themes"):
        out += [f"## {heading}", "", existing.get(heading, "Pending."), ""]

    out += ["## Papers", "", "| Date | Name | Venue | Title | Code |", "|---|---|---|---|---|"]
    for row in rows:
        out.append(
            f"| {row['date']} | {row['name']} | {row['venue']} "
            f"| {row['title']} | {row['code']} |"
        )
    out.append("")

    out += ["## Notable entries", "", existing.get("Notable entries", "Pending."), ""]

    have_summaries = existing.get("Paper summaries")
    if rebuild or not have_summaries:
        body = render_summaries(rows, meta, summarizer)
    else:
        body = have_summaries
    if body.strip():
        out += ["## Paper summaries", "", body, ""]

    out += ["## See also", ""]
    out += ["- [Wiki index](../../index.md)"]
    if prev_slug and prev_title:
        out += [f"- [Previous: {prev_title}]({prev_slug}.md)"]
    if next_slug and next_title:
        out += [f"- [Next: {next_title}]({next_slug}.md)"]
    out += [""]

    return "\n".join(out)


def render_index_table(sections: list[dict]) -> str:
    lines = ["| # | Section | Papers |", "|---|---|---|"]
    for s in sections:
        lines.append(
            f"| {s['index']:02d} | [{s['title']}](raw/papers/{s['slug']}.md) | {len(s['rows'])} |"
        )
    return "\n".join(lines)


def update_index(sections: list[dict]) -> None:
    """Patch the AI4CHIPS section of wiki/index.md between markers."""
    path = WIKI_DIR / "index.md"
    total = sum(len(s["rows"]) for s in sections)
    table = render_index_table(sections)
    content = f"## AI4CHIPS Sections\n\nThe index holds {total} papers in {len(sections)} sections.\n\n{table}\n"

    if not path.exists():
        # Create the file with markers if it does not exist
        text = (
            "# Wiki Index\n\n"
            "<!-- generated:references:ai4chips -->\n"
            f"{content}"
            "<!-- /generated:references:ai4chips -->\n\n"
            "<!-- generated:references:neuromorphic -->\n"
            "<!-- /generated:references:neuromorphic -->\n"
        )
        path.write_text(text, encoding="utf-8")
        return

    text = path.read_text(encoding="utf-8")
    start_marker = "<!-- generated:references:ai4chips -->"
    end_marker = "<!-- /generated:references:ai4chips -->"

    if start_marker in text and end_marker in text:
        # Replace between markers
        pattern = re.compile(
            re.escape(start_marker) + r".*?" + re.escape(end_marker),
            re.S
        )
        text = pattern.sub(
            start_marker + "\n" + content + end_marker,
            text
        )
    else:
        # Append markers if missing
        text = text.rstrip() + f"\n\n{start_marker}\n{content}{end_marker}\n"

    path.write_text(text, encoding="utf-8")


# --------------------------------------------------------------------------- #
# checks
# --------------------------------------------------------------------------- #
FIXTURE = """# head
<details><summary><h2 style="display: inline;">Flow & Layout</h2></summary>

Date|Method|Type|Conference|Paper Title and Paper Interpretation (In Chinese)|Code
-----|----|-----|-----|-----|-----
2023-01-16|[Thing](https://arxiv.org/abs/2211.16495)|![b](https://img.shields.io/x)|DAC 2023 (pp. 1-2)|A title with an em dash — here|[c](https://github.com/x)
2024-03|[](https://eprint.iacr.org/2023/212.pdf)|![b](https://img.shields.io/x)|||
</details>
"""


def selftest() -> None:
    sections = parse_sections(FIXTURE)
    assert len(sections) == 1, sections
    s = sections[0]
    assert s["slug"] == "01-flow-and-layout", s["slug"]
    assert s["title"] == "Flow & Layout", s["title"]

    rows = s["rows"]
    assert len(rows) == 2, rows

    first = rows[0]
    assert first["name"] == "[Thing](https://arxiv.org/abs/2211.16495)", first["name"]
    assert first["venue"] == "DAC 2023 (pp. 1-2)", first["venue"]
    assert "—" not in first["title"], "em dash survived scrubbing"
    assert first["arxiv"] == ["2211.16495"], first["arxiv"]
    assert first["code"] == "[c](https://github.com/x)", first["code"]

    second = rows[1]
    assert second["name"] == "[paper](https://eprint.iacr.org/2023/212.pdf)", second["name"]
    assert second["venue"] == EMPTY_CELL, second["venue"]
    assert second["title"] == EMPTY_CELL, second["title"]
    assert second["arxiv"] == [], second["arxiv"]

    # An empty cell must never render as a dash, and prose must keep its words.
    assert scrub_dashes("a – b") == "a to b"
    assert first_sentences("One. Two. Three.") == "One. Two."

    # With no model the summarizer must stay offline and use the abstract.
    plain = Summarizer(None)
    entry = {"title": "T", "abstract": "One. Two. Three."}
    assert plain.summarize("2211.16495", entry) == "One. Two."
    assert plain.calls == 0, "no model must mean no request"

    # A page rebuild must keep model-written prose and regenerate the table.
    sections[0]["_prev_slug"] = "01-flow-and-layout"
    sections[0]["_prev_title"] = "Flow & Layout"
    sections[0]["_next_slug"] = "02-hls"
    sections[0]["_next_title"] = "HLS"
    page = render_page(sections[0], {}, "01-flow-and-layout", False, plain)
    assert "---" in page, "frontmatter missing"
    assert "title: Flow & Layout" in page, "title in frontmatter missing"
    assert "type: reference" in page, "type in frontmatter missing"
    assert "tags: [reference, generated, benchmark]" in page, "tags in frontmatter missing"
    assert "## Papers" in page
    assert "| 2023-01-16 |" in page
    assert "largest section" in page
    assert "## See also" in page, "See also section missing"
    assert "[Wiki index](../../index.md)" in page, "index link missing"
    assert "[Previous: Flow & Layout]" in page, "previous section link missing"
    assert "[Next: HLS]" in page, "next section link missing"
    assert "—" not in page and "–" not in page, "dash reached the output"

    print("selftest ok")


# --------------------------------------------------------------------------- #
def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--offline", action="store_true", help="use cached downloads only")
    ap.add_argument(
        "--rebuild-summaries",
        action="store_true",
        help="regenerate the Paper summaries section from abstracts",
    )
    ap.add_argument("--selftest", action="store_true", help="run parser checks and exit")
    ap.add_argument(
        "--model",
        default=None,
        help=(
            "Ollama model that writes the summaries, for example "
            f"{OLLAMA_MODEL} or glm-5.3-flash:cloud. Without this flag the "
            "script takes the opening sentences of each abstract instead."
        ),
    )
    ap.add_argument("--ollama-url", default=OLLAMA_URL, help="Ollama base URL")
    args = ap.parse_args()

    if args.selftest:
        selftest()
        return

    print("fetching source index")
    readme = fetch(SOURCE_URL, "AI4CHIPS_README.md", args.offline)
    sections = parse_sections(readme)
    total = sum(len(s["rows"]) for s in sections)
    print(f"parsed {len(sections)} sections, {total} papers")

    ids = sorted({aid for s in sections for r in s["rows"] for aid in r["arxiv"]})
    print(f"fetching arXiv metadata for {len(ids)} ids")
    meta = fetch_arxiv(ids, args.offline)
    print(f"have metadata for {len(meta)} papers")

    summarizer = Summarizer(args.model, args.ollama_url)
    if args.model:
        print(f"writing summaries with {args.model} via Ollama")

    largest = max(sections, key=lambda s: len(s["rows"]))["slug"]
    WIKI_DIR.mkdir(parents=True, exist_ok=True)
    REFERENCES_DIR.mkdir(parents=True, exist_ok=True)
    try:
        for i, s in enumerate(sections):
            # Inject previous and next section info for See also ring links
            # Create a ring where the last section links back to the first
            s["_prev_slug"] = sections[i - 1]["slug"]
            s["_prev_title"] = sections[i - 1]["title"]
            s["_next_slug"] = sections[(i + 1) % len(sections)]["slug"]
            s["_next_title"] = sections[(i + 1) % len(sections)]["title"]
            path = REFERENCES_DIR / f"{s['slug']}.md"
            page = render_page(s, meta, largest, args.rebuild_summaries, summarizer)
            path.write_text(page, encoding="utf-8")
            covered = sum(1 for r in s["rows"] for a in r["arxiv"] if a in meta)
            print(f"  {path.name}: {len(s['rows'])} papers, {covered} with an abstract")
            # Checkpoint after every page. A model run costs minutes per page, so
            # a kill between pages must not discard the answers already paid for.
            summarizer.save()
    finally:
        summarizer.save()

    if args.model:
        print(f"model calls: {summarizer.calls}, fallbacks: {summarizer.failures}")

    update_index(sections)

    # Append to log
    from datetime import date
    log_path = WIKI_DIR / "log.md"
    today = date.today().isoformat()
    log_entry = f"## [{today}] update | AI4CHIPS reference pages\n\n- Rebuilt {len(sections)} reference pages under raw/papers/\n"
    if log_path.exists():
        log_path.write_text(log_path.read_text(encoding="utf-8") + "\n" + log_entry, encoding="utf-8")
    else:
        # Create log if it does not exist
        preamble = (
            "# Wiki Log\n\n"
            "> Chronological record of all wiki actions. Append-only.\n"
            "> Format: `## [YYYY-MM-DD] action | subject`\n"
            "> Actions: ingest, update, query, lint, create, archive, delete\n"
            "> Body: list only files actually created or updated. Skip files that were\n"
            "> inspected, considered, or deliberately left unchanged, and do not narrate\n"
            "> decisions about what not to do. Aim for roughly 20 lines per entry.\n"
            "> When this file exceeds 500 entries, rotate: rename to log-YYYY.md, start fresh.\n\n"
        )
        log_path.write_text(preamble + log_entry, encoding="utf-8")

    stray = [
        p.name
        for p in sorted(WIKI_DIR.glob("*.md"))
        if any(d in p.read_text(encoding="utf-8") for d in DASHES)
    ]
    if stray:
        print(f"warning: em or en dash present in {', '.join(stray)}", file=sys.stderr)
    print(f"done: {total} papers in {len(sections)} pages")


if __name__ == "__main__":
    main()
