#!/usr/bin/env python3
"""Download cited arXiv PDFs into wiki/raw/papers and print their metadata.

Takes arXiv ids, or wiki pages to scan for arxiv.org/abs|pdf links. Each PDF
is saved as wiki/raw/papers/<id>.pdf (git-ignored), checked for the %PDF
header, and skipped if it already exists. Titles and abstracts come from the
arXiv export API, so a page can be checked against what the id really is.

Usage:
    python tools/fetch_arxiv.py 1804.07858 2105.03649
    python tools/fetch_arxiv.py --from-page wiki/summaries/on-chip-learning-for-snn-hardware.md
    python tools/fetch_arxiv.py --selftest
"""

from __future__ import annotations

import argparse
import re
import time
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAPERS = ROOT / "wiki" / "raw" / "papers"
ID_RE = re.compile(r"arxiv\.org/(?:abs|pdf)/(\d{4}\.\d{4,5})")
ATOM = "{http://www.w3.org/2005/Atom}"
UA = {"User-Agent": "Infer-chip wiki fetch (arXiv PDF mirror for citations)"}


def ids_from_text(text: str) -> list[str]:
    return sorted(set(ID_RE.findall(text)))


def _get(url: str) -> bytes:
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60) as r:
        return r.read()


def fetch_pdf(aid: str, delay_s: float = 3.0) -> str:
    """Return 'existing', 'saved' or 'failed: <reason>'."""
    dst = PAPERS / f"{aid}.pdf"
    if dst.exists() and dst.read_bytes()[:4] == b"%PDF":
        return "existing"
    try:
        data = _get(f"https://arxiv.org/pdf/{aid}")
    except OSError as exc:
        return f"failed: {exc}"
    finally:
        time.sleep(delay_s)  # arXiv asks for at most one request every 3 s
    if data[:4] != b"%PDF":
        return "failed: not a PDF"
    dst.write_bytes(data)
    return "saved"


def parse_atom(xml: bytes) -> dict[str, dict]:
    out = {}
    for e in ET.fromstring(xml).iter(f"{ATOM}entry"):
        m = re.search(r"(\d{4}\.\d{4,5})", e.findtext(f"{ATOM}id", ""))
        if m:
            clean = lambda s: " ".join((s or "").split())  # noqa: E731
            out[m.group(1)] = {"title": clean(e.findtext(f"{ATOM}title")),
                               "abstract": clean(e.findtext(f"{ATOM}summary")),
                               "published": (e.findtext(f"{ATOM}published") or "")[:10]}
    return out


def fetch_meta(ids: list[str]) -> dict[str, dict]:
    return parse_atom(_get("https://export.arxiv.org/api/query?max_results=100&id_list="
                           + ",".join(ids)))


def selftest() -> None:
    assert ids_from_text("see https://arxiv.org/abs/1804.07858 and arxiv.org/pdf/2105.03649v2 "
                         "and https://arxiv.org/abs/1804.07858") == ["1804.07858", "2105.03649"]
    xml = (b'<feed xmlns="http://www.w3.org/2005/Atom"><entry>'
           b"<id>http://arxiv.org/abs/1804.07858v4</id><title>A 0.086-mm2\n ODIN</title>"
           b"<summary> text </summary><published>2018-04-21T00:00:00Z</published>"
           b"</entry></feed>")
    assert parse_atom(xml) == {"1804.07858": {"title": "A 0.086-mm2 ODIN", "abstract": "text",
                                              "published": "2018-04-21"}}
    print("selftest ok")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("ids", nargs="*")
    ap.add_argument("--from-page", action="append", default=[], type=Path)
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()
    if args.selftest:
        return selftest()
    ids = sorted(set(args.ids) | {i for p in args.from_page for i in ids_from_text(p.read_text())})
    meta = fetch_meta(ids) if ids else {}
    print("| arXiv id | Title | Published | PDF |\n|---|---|---|---|")
    for aid in ids:
        m = meta.get(aid, {})
        print(f"| {aid} | {m.get('title', 'NOT FOUND ON ARXIV')} | {m.get('published', '')} "
              f"| {fetch_pdf(aid)} |")


if __name__ == "__main__":
    main()
