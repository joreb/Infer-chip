#!/usr/bin/env python3
"""Ingest the Open Neuromorphic resource list into the wiki.

Source: raw/open-neuromorphic/README.md (clone it into raw/ first).

The source list mixes two layouts. The software sections hold an HTML table
where each row carries a logo, a GitHub stars badge and a prose description.
The hardware section holds one "###" heading per project. This script reads
both, asks an Ollama model for an ASD-STE100 summary of each entry, and writes
one page per section under wiki/neuromorphic/ with its own index.

Summaries are cached by model and entry, so a rerun costs nothing for entries
that already have one.

Usage:
    python tools/ingest_neuromorphic.py --model glm-5.3-flash:cloud
    python tools/ingest_neuromorphic.py                 # no model: source prose
    python tools/ingest_neuromorphic.py --selftest
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

from build_wiki import OLLAMA_URL, Summarizer, scrub_dashes, slugify

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "raw" / "open-neuromorphic" / "README.md"
WIKI_DIR = ROOT / "wiki"
REFERENCES_DIR = WIKI_DIR / "references"
SOURCE_REPO = "https://github.com/open-neuromorphic/open-neuromorphic"
SOURCE_SITE = "https://open-neuromorphic.org"

HTML_LINE_RE = re.compile(r"^\s*</?(?:table|tr|td|a|img|br|p|div)\b", re.I)
BADGE_RE = re.compile(r"!\[[^\]]*\]\([^)]*\)")
STARS_RE = re.compile(r"img\.shields\.io/github/stars/([A-Za-z0-9_.-]+)/([A-Za-z0-9_.-]+)")
LINK_RE = re.compile(r"\[([^\]]+)\]\((https?://[^)]+)\)")
SECTION_RE = re.compile(r"^## (?P<name>.+?)\s*$", re.M)


def strip_markup(block: str) -> str:
    """Drop HTML scaffolding and badges, keep the prose."""
    lines = []
    for line in block.splitlines():
        if HTML_LINE_RE.match(line) or "shields.io" in line or "<img" in line:
            continue
        lines.append(BADGE_RE.sub("", line))
    return " ".join(" ".join(lines).split()).strip()


def entry_from_block(block: str, fallback_name: str | None = None) -> dict | None:
    prose = strip_markup(block)
    if len(prose) < 40:
        return None
    link = LINK_RE.search(prose)
    name = fallback_name or (link.group(1) if link else "")
    if not name:
        return None
    stars = STARS_RE.search(block)
    return {
        "name": name.strip(),
        "url": link.group(2) if link else SOURCE_SITE,
        "repo": f"https://github.com/{stars.group(1)}/{stars.group(2)}" if stars else "",
        "description": prose,
    }


def parse(text: str) -> list[dict]:
    """Return [{name, slug, entries}] for each "##" section after the heading."""
    bounds = [(m.start(), m.group("name")) for m in SECTION_RE.finditer(text)]
    bounds = [(s, n) for s, n in bounds if n.lower() != "list of resources"]
    sections = []
    for i, (start, name) in enumerate(bounds):
        end = bounds[i + 1][0] if i + 1 < len(bounds) else len(text)
        body = text[start:end]
        entries: list[dict] = []

        # Hardware layout: one "###" heading per project.
        parts = re.split(r"^### +(.+?)\s*$", body, flags=re.M)
        if len(parts) > 1:
            for heading, chunk in zip(parts[1::2], parts[2::2]):
                entry = entry_from_block(chunk, fallback_name=heading)
                if entry:
                    entries.append(entry)
        else:
            # Software layout: one <tr> per framework.
            for row in re.split(r"<tr>", body, flags=re.I)[1:]:
                entry = entry_from_block(row)
                if entry:
                    entries.append(entry)

        if entries:
            sections.append({"name": name, "slug": slugify(name), "entries": entries})
    return sections


def render(section: dict, summarizer: Summarizer, prev_slug: str = "", prev_title: str = "", next_slug: str = "", next_title: str = "") -> str:
    # Add tags: basic tag list is [reference, generated, neuromorphic]
    # Add snn tag if section is about spiking neural networks
    tags = ["reference", "generated", "neuromorphic"]
    if "spiking" in section["slug"].lower() or "snn" in section["slug"].lower():
        tags.append("snn")
    tags_str = ", ".join(tags)

    frontmatter = [
        "---",
        f"title: {section['name']}",
        "created: 2026-10-17",
        "updated: 2026-10-17",
        "type: reference",
        f"tags: [{tags_str}]",
        "sources: []",
        "---",
        "",
    ]

    out = frontmatter + [
        f"# {section['name']}",
        "",
        f"> Section of the [Open Neuromorphic resource list]({SOURCE_REPO}). "
        f"{len(section['entries'])} entries.",
        "",
    ]
    for e in section["entries"]:
        summary = summarizer.summarize(
            f"onm:{section['slug']}:{slugify(e['name'])}",
            {"title": e["name"], "abstract": e["description"]},
        )
        links = [f"[project page]({e['url']})"]
        if e["repo"]:
            links.append(f"[repository]({e['repo']})")
        out += [
            f"## {e['name']}",
            "",
            scrub_dashes(summary),
            "",
            " and ".join(links) + ".",
            "",
        ]

    out += ["## See also", ""]
    out += ["- [Wiki index](../index.md)"]
    if prev_slug and prev_title:
        out += [f"- [Previous: {prev_title}]({prev_slug}.md)"]
    if next_slug and next_title:
        out += [f"- [Next: {next_title}]({next_slug}.md)"]
    out += [""]

    return "\n".join(out)


def update_index(sections: list[dict]) -> None:
    """Patch the Open Neuromorphic section of wiki/index.md between markers."""
    path = WIKI_DIR / "index.md"
    total = sum(len(s["entries"]) for s in sections)
    table_lines = ["| Section | Entries |", "|---|---|"]
    for s in sections:
        table_lines.append(f"| [onm-{s['slug']}](references/onm-{s['slug']}.md) | {len(s['entries'])} |")
    table = "\n".join(table_lines)
    content = f"## Open Neuromorphic Sections\n\nThe index holds {total} entries in {len(sections)} sections.\n\n{table}\n"

    if not path.exists():
        # Create the file with markers if it does not exist
        text = (
            "# Wiki Index\n\n"
            "<!-- generated:references:ai4chips -->\n"
            "<!-- /generated:references:ai4chips -->\n\n"
            "<!-- generated:references:neuromorphic -->\n"
            f"{content}"
            "<!-- /generated:references:neuromorphic -->\n"
        )
        path.write_text(text, encoding="utf-8")
        return

    text = path.read_text(encoding="utf-8")
    start_marker = "<!-- generated:references:neuromorphic -->"
    end_marker = "<!-- /generated:references:neuromorphic -->"

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


FIXTURE = """# List of resources

## SNN training frameworks for ML

Open-source software to train spiking neural networks for ML tasks.

<table>
<tr>
<td>
<a href="https://x.org/bindsnet/"><img src="images/bindsnet.jpg" alt="b" width="1000px"/></a>

![GitHub Repo stars](https://img.shields.io/github/stars/bindsnet/bindsnet?style=social)
</td>
<td>

[BindsNET](https://x.org/bindsnet/) is built on top of the PyTorch deep learning platform. It simulates spiking neural networks and targets machine learning.

</td>
</tr>
</table>

## Digital hardware projects

Open-source digital hardware projects.

### ODIN Spiking Neural Network (SNN) Processor

<img src="images/odin.png" alt="odin" width="500"/>

[ODIN](https://x.org/odin/) is an online-learning digital spiking neuromorphic processor prototyped in 28-nm FDSOI CMOS. It uses a single 256-neuron crossbar core.
"""


def selftest() -> None:
    sections = parse(FIXTURE)
    assert len(sections) == 2, [s["name"] for s in sections]

    soft, hard = sections
    assert soft["slug"] == "snn-training-frameworks-for-ml", soft["slug"]
    assert len(soft["entries"]) == 1, soft["entries"]
    e = soft["entries"][0]
    assert e["name"] == "BindsNET", e["name"]
    assert e["repo"] == "https://github.com/bindsnet/bindsnet", e["repo"]
    assert "PyTorch" in e["description"]
    assert "shields.io" not in e["description"], "badge leaked into the prose"
    assert "<img" not in e["description"], "HTML leaked into the prose"

    assert len(hard["entries"]) == 1, hard["entries"]
    h = hard["entries"][0]
    assert h["name"] == "ODIN Spiking Neural Network (SNN) Processor", h["name"]
    assert h["repo"] == "", "no stars badge means no repository link"

    plain = Summarizer(None)
    page = render(soft, plain, "onm-digital-hardware-projects", "Digital hardware projects", "onm-digital-hardware-projects", "Digital hardware projects")
    assert "---" in page, "frontmatter missing"
    assert "title: SNN training frameworks for ML" in page, "title in frontmatter missing"
    assert "type: reference" in page, "type in frontmatter missing"
    assert "tags: [reference, generated, neuromorphic, snn]" in page, "tags in frontmatter missing"
    assert "## BindsNET" in page
    assert "[repository](https://github.com/bindsnet/bindsnet)" in page
    assert "## See also" in page, "See also section missing"
    assert "[Wiki index](../index.md)" in page, "index link missing"
    assert "[Previous: Digital hardware projects]" in page, "previous section link missing"
    assert "[Next: Digital hardware projects]" in page, "next section link missing"
    assert plain.calls == 0, "no model must mean no request"
    assert "—" not in page and "–" not in page

    print("selftest ok")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--model", default=None, help="Ollama model, e.g. glm-5.3-flash:cloud")
    ap.add_argument("--ollama-url", default=OLLAMA_URL)
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()

    if args.selftest:
        selftest()
        return

    if not SOURCE.exists():
        raise SystemExit(
            f"missing {SOURCE}. Clone it first:\n"
            f"  git clone --depth 1 {SOURCE_REPO}.git raw/open-neuromorphic"
        )

    sections = parse(SOURCE.read_text(encoding="utf-8", errors="replace"))
    total = sum(len(s["entries"]) for s in sections)
    print(f"parsed {len(sections)} sections, {total} entries")

    summarizer = Summarizer(args.model, args.ollama_url)
    if args.model:
        print(f"writing summaries with {args.model} via Ollama")

    REFERENCES_DIR.mkdir(parents=True, exist_ok=True)
    try:
        for i, s in enumerate(sections):
            # Inject previous and next section info for See also ring links
            # Create a ring where the last section links back to the first
            prev_slug = f"onm-{sections[i - 1]['slug']}"
            prev_title = sections[i - 1]["name"]
            next_slug = f"onm-{sections[(i + 1) % len(sections)]['slug']}"
            next_title = sections[(i + 1) % len(sections)]["name"]

            path = REFERENCES_DIR / f"onm-{s['slug']}.md"
            path.write_text(render(s, summarizer, prev_slug, prev_title, next_slug, next_title), encoding="utf-8")
            print(f"  {path.name}: {len(s['entries'])} entries")
    finally:
        summarizer.save()

    update_index(sections)

    # Append to log
    from datetime import date
    log_path = WIKI_DIR / "log.md"
    today = date.today().isoformat()
    log_entry = f"## [{today}] update | Open Neuromorphic reference pages\n\n- Rebuilt {len(sections)} reference pages under references/\n"
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

    if args.model:
        print(f"model calls: {summarizer.calls}, fallbacks: {summarizer.failures}")
    print(f"done: {total} entries in {len(sections)} pages under {REFERENCES_DIR.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
