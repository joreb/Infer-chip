#!/usr/bin/env python3
"""Pull every referenced PDF and git repository into raw/.

Sources scanned:
  raw/open-neuromorphic/README.md        the Open Neuromorphic resource list
  tools/.cache/AI4CHIPS_README.md        the AI4CHIPS paper index (built by
                                         build_wiki.py; downloaded if absent)
  wiki/*.md                              the generated wiki pages

Layout produced:
  raw/pdf/<arxiv-id>.pdf                 arXiv papers
  raw/pdf/other/<host>__<name>.pdf       other PDF links
  raw/git/<owner>__<repo>/               shallow clones
  raw/manifest.json                      what was fetched, skipped and failed

Everything is skip-if-present, so a rerun only fetches what is missing. raw/ is
git-ignored because it is large and this script reproduces it.

Usage:
    python tools/fetch_raw.py                  # fetch PDFs and clone repos
    python tools/fetch_raw.py --pdf-only
    python tools/fetch_raw.py --git-only
    python tools/fetch_raw.py --limit 20       # try the first 20 of each kind
    python tools/fetch_raw.py --dry-run        # list targets, fetch nothing
    python tools/fetch_raw.py --selftest
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "raw"
PDF_DIR = RAW / "pdf"
OTHER_PDF_DIR = PDF_DIR / "other"
GIT_DIR = RAW / "git"
CACHE_DIR = Path(__file__).resolve().parent / ".cache"
MANIFEST = RAW / "manifest.json"

AI4CHIPS_URL = "https://raw.githubusercontent.com/Archerll/AI4CHIPSpaper/main/README.md"

ARXIV_RE = re.compile(r"arxiv\.org/(?:abs|pdf)/(\d{4}\.\d{4,5})")
PDF_RE = re.compile(r"https?://[^\s)\"'<>]+?\.pdf", re.I)
GITHUB_RE = re.compile(
    r"https?://github\.com/([A-Za-z0-9_.-]+)/([A-Za-z0-9_.-]+?)(?:\.git)?(?=[)\s\"'<>#?]|/tree/|/blob/|$)"
)

# Repositories that are infrastructure, not referenced source material.
SKIP_REPOS = {("Archerll", "AI4CHIPSpaper")}

ARXIV_DELAY_S = 3.0  # arXiv asks for one bulk request every few seconds
PDF_DELAY_S = 1.0
TIMEOUT_S = 120
USER_AGENT = "ai4chips-wiki-builder/1.0 (research use; contact via repository)"


def sources() -> list[tuple[str, str]]:
    """Return (label, text) for every file that may hold references."""
    out: list[tuple[str, str]] = []

    onm = RAW / "open-neuromorphic" / "README.md"
    if onm.exists():
        out.append((str(onm.relative_to(ROOT)), onm.read_text(encoding="utf-8", errors="replace")))

    ai4 = CACHE_DIR / "AI4CHIPS_README.md"
    if not ai4.exists():
        CACHE_DIR.mkdir(parents=True, exist_ok=True)
        print("AI4CHIPS README not cached, downloading")
        ai4.write_text(http_text(AI4CHIPS_URL), encoding="utf-8")
    out.append((str(ai4.relative_to(ROOT)), ai4.read_text(encoding="utf-8")))

    wiki = ROOT / "wiki"
    if wiki.is_dir():
        for page in sorted(wiki.glob("*.md")):
            out.append((str(page.relative_to(ROOT)), page.read_text(encoding="utf-8")))

    if not out:
        raise SystemExit("no sources found: clone open-neuromorphic or build the wiki first")
    return out


def http_text(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=TIMEOUT_S) as r:
        return r.read().decode("utf-8", errors="replace")


# --------------------------------------------------------------------------- #
# extraction
# --------------------------------------------------------------------------- #
def safe_name(url: str) -> str:
    """Build a filesystem-safe name for a non-arXiv PDF URL."""
    cleaned = re.sub(r"^https?://", "", url)
    host = cleaned.split("/", 1)[0].replace(":", "_")
    tail = cleaned.rsplit("/", 1)[-1] or "document.pdf"
    tail = re.sub(r"[^A-Za-z0-9._-]+", "_", tail)
    if not tail.lower().endswith(".pdf"):
        tail += ".pdf"
    return f"{host}__{tail}"[:150]


def collect(texts: list[tuple[str, str]]) -> dict:
    arxiv: dict[str, str] = {}
    other_pdf: dict[str, str] = {}
    repos: dict[tuple[str, str], str] = {}

    for label, text in texts:
        for aid in ARXIV_RE.findall(text):
            arxiv.setdefault(aid, label)
        for url in PDF_RE.findall(text):
            if "arxiv.org" in url.lower():
                continue  # handled by the arXiv id path
            other_pdf.setdefault(url.rstrip(".,"), label)
        for owner, repo in GITHUB_RE.findall(text):
            key = (owner, repo)
            if key in SKIP_REPOS:
                continue
            repos.setdefault(key, label)

    return {"arxiv": arxiv, "other_pdf": other_pdf, "repos": repos}


# --------------------------------------------------------------------------- #
# fetching
# --------------------------------------------------------------------------- #
def download(url: str, dest: Path) -> tuple[bool, str]:
    if dest.exists() and dest.stat().st_size > 1024:
        return True, "skip"
    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp = dest.with_suffix(dest.suffix + ".part")
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT_S) as r:
            data = r.read()
    except (urllib.error.URLError, TimeoutError, ConnectionError) as exc:
        return False, str(exc)[:120]
    if len(data) < 1024:
        return False, f"too small ({len(data)} bytes)"
    if not data.startswith(b"%PDF"):
        return False, "not a PDF (login wall or HTML error page)"
    tmp.write_bytes(data)
    tmp.replace(dest)
    return True, "fetched"


def clone(owner: str, repo: str) -> tuple[bool, str]:
    dest = GIT_DIR / f"{owner}__{repo}"
    if (dest / ".git").is_dir():
        return True, "skip"
    dest.parent.mkdir(parents=True, exist_ok=True)
    proc = subprocess.run(
        [
            "git",
            "clone",
            "--depth",
            "1",
            "--quiet",
            f"https://github.com/{owner}/{repo}.git",
            str(dest),
        ],
        capture_output=True,
        text=True,
        timeout=600,
    )
    if proc.returncode != 0:
        err = (proc.stderr or proc.stdout or "clone failed").strip().splitlines()
        return False, (err[-1] if err else "clone failed")[:120]
    return True, "cloned"


# --------------------------------------------------------------------------- #
def selftest() -> None:
    text = """
    see [paper](https://arxiv.org/pdf/2504.03711) and [abs](https://arxiv.org/abs/2211.16495)
    plus [local](https://www.cse.cuhk.edu.hk/~byu/papers/J119-TCAD2025-FGNN2.pdf),
    code at https://github.com/NVlabs/verilog-eval and
    [RTL-Coder](https://github.com/hkustzhiyao/RTL-Coder.git),
    a tree link https://github.com/foo/bar/tree/main/src
    and the index itself https://github.com/Archerll/AI4CHIPSpaper
    """
    got = collect([("fixture", text)])

    assert set(got["arxiv"]) == {"2504.03711", "2211.16495"}, got["arxiv"]
    assert len(got["other_pdf"]) == 1, got["other_pdf"]
    assert all("arxiv" not in u for u in got["other_pdf"]), got["other_pdf"]

    repos = set(got["repos"])
    assert ("NVlabs", "verilog-eval") in repos, repos
    assert ("hkustzhiyao", "RTL-Coder") in repos, "the .git suffix must be stripped"
    assert ("foo", "bar") in repos, "a /tree/ link must resolve to the repo"
    assert ("Archerll", "AI4CHIPSpaper") not in repos, "the index repo must be skipped"

    name = safe_name("https://www.cse.cuhk.edu.hk/~byu/papers/J119-TCAD2025-FGNN2.pdf")
    assert name == "www.cse.cuhk.edu.hk__J119-TCAD2025-FGNN2.pdf", name
    assert "/" not in name and "\\" not in name

    print("selftest ok")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--pdf-only", action="store_true")
    ap.add_argument("--git-only", action="store_true")
    ap.add_argument("--limit", type=int, default=0, help="cap targets per kind")
    ap.add_argument("--dry-run", action="store_true", help="list targets only")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()

    if args.selftest:
        selftest()
        return

    found = collect(sources())
    arxiv = sorted(found["arxiv"])
    other = sorted(found["other_pdf"])
    repos = sorted(found["repos"])
    if args.limit:
        arxiv, other, repos = arxiv[: args.limit], other[: args.limit], repos[: args.limit]

    print(f"targets: {len(arxiv)} arXiv PDFs, {len(other)} other PDFs, {len(repos)} repos")
    if args.dry_run:
        for aid in arxiv:
            print(f"  arxiv {aid}")
        for url in other:
            print(f"  pdf   {url}")
        for owner, repo in repos:
            print(f"  git   {owner}/{repo}")
        return

    results: dict[str, dict] = {"arxiv": {}, "other_pdf": {}, "repos": {}}

    if not args.git_only:
        for i, aid in enumerate(arxiv, start=1):
            ok, note = download(f"https://arxiv.org/pdf/{aid}", PDF_DIR / f"{aid}.pdf")
            results["arxiv"][aid] = note if ok else f"FAIL: {note}"
            print(f"  [{i}/{len(arxiv)}] arxiv {aid}: {results['arxiv'][aid]}")
            if note == "fetched":
                time.sleep(ARXIV_DELAY_S)

        for i, url in enumerate(other, start=1):
            ok, note = download(url, OTHER_PDF_DIR / safe_name(url))
            results["other_pdf"][url] = note if ok else f"FAIL: {note}"
            print(f"  [{i}/{len(other)}] pdf {safe_name(url)}: {results['other_pdf'][url]}")
            if note == "fetched":
                time.sleep(PDF_DELAY_S)

    if not args.pdf_only:
        for i, (owner, repo) in enumerate(repos, start=1):
            try:
                ok, note = clone(owner, repo)
            except subprocess.TimeoutExpired:
                ok, note = False, "clone timed out"
            results["repos"][f"{owner}/{repo}"] = note if ok else f"FAIL: {note}"
            print(f"  [{i}/{len(repos)}] git {owner}/{repo}: {results['repos'][f'{owner}/{repo}']}")

    RAW.mkdir(parents=True, exist_ok=True)
    MANIFEST.write_text(json.dumps(results, indent=1, sort_keys=True), encoding="utf-8")

    for kind, rows in results.items():
        failed = [k for k, v in rows.items() if str(v).startswith("FAIL")]
        done = len(rows) - len(failed)
        print(f"{kind}: {done} present, {len(failed)} failed")
        for k in failed[:10]:
            print(f"    {k}: {rows[k]}", file=sys.stderr)
    print(f"manifest: {MANIFEST.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
