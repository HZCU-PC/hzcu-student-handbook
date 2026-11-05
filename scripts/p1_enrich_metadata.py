"""Fill placeholder authors/links from curated evidence + arXiv API."""
from __future__ import annotations

import argparse
import ast
import json
import re
import time
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "docs" / "papers.md"
PATTERN = re.compile(
    r'(<script id="papers-json" type="application/json">)(.*?)(</script>)', re.S
)
PLACEHOLDER_AUTHORS = "作者信息见原论文"

ALIASES: dict[str, str] = {
    "ERNIE 3.0": "ERNIE3",
    "AlphaFold 3": "AlphaFold3",
    "LDM / Stable Diffusion": "潜在扩散 LDM",
    "缩放定律": "Scaling Laws",
    "LLaMA": "Llama 4",
    "Mamba": "MiniMax-01",
    "Llama 3": "Llama3",
    "PaLM 2": "PaLM 2",
    "Gemini 1.5": "Gemini",
    "DALL·E 2": "DALL·E",
    "DALL·E 3": "DALL·E",
}


def load_evidence() -> dict[str, tuple]:
    src = (ROOT / "scripts" / "expand_papers_from_workbook.py").read_text(encoding="utf-8")
    m = re.search(r"^evidence = (\{.*?\n\})\nhooks=", src, re.M | re.S)
    if not m:
        raise SystemExit("evidence block not found in expand_papers_from_workbook.py")
    return ast.literal_eval(m.group(1))


def needs_enrich(p: dict) -> bool:
    if PLACEHOLDER_AUTHORS in (p.get("authors") or ""):
        return True
    return "arxiv.org/search" in (p.get("link") or "").lower()


def evidence_key(zh: str, ev: dict) -> str | None:
    if zh in ev:
        return zh
    if zh in ALIASES and ALIASES[zh] in ev:
        return ALIASES[zh]
    for k in ev:
        if k.lower() == zh.lower():
            return k
    return None


def apply_evidence(p: dict, ev: dict) -> bool:
    key = evidence_key(p.get("zh") or "", ev)
    if not key:
        return False
    link, en, authors, *_ = ev[key]
    p["link"] = link
    p["en"] = en
    p["authors"] = authors
    if "arxiv.org" in link or "doi.org" in link:
        p["venue"] = "arXiv / 原始论文" if "arxiv" in link else "原始论文"
    return True


def _tokens(s: str) -> set[str]:
    return {w for w in re.sub(r"[^\w\s]", " ", (s or "").lower()).split() if len(w) > 1}


def title_score(want: str, got: str) -> float:
    a, b = _tokens(want), _tokens(got)
    if not a:
        return 0.0
    return len(a & b) / len(a)


def arxiv_lookup(title: str, year: int | None) -> tuple[str, str, str] | None:
    q = urllib.parse.quote(f'all:"{title}"')
    url = f"http://export.arxiv.org/api/query?search_query={q}&max_results=5"
    for attempt in range(4):
        try:
            with urllib.request.urlopen(url, timeout=25) as resp:
                raw = resp.read()
            break
        except urllib.error.HTTPError as e:
            if e.code == 429 and attempt < 3:
                time.sleep(2.0 * (attempt + 1))
                continue
            raise
    root = ET.fromstring(raw)
    ns = {"a": "http://www.w3.org/2005/Atom"}
    best = None
    best_score = 0.0
    for entry in root.findall("a:entry", ns):
        t_el = entry.find("a:title", ns)
        id_el = entry.find("a:id", ns)
        if t_el is None or id_el is None:
            continue
        got_title = " ".join(t_el.text.split())
        score = title_score(title, got_title)
        pub = entry.find("a:published", ns)
        pub_year = int(pub.text[:4]) if pub is not None and pub.text else None
        if year and pub_year and abs(pub_year - year) > 2:
            score *= 0.5
        if score > best_score:
            best_score = score
            names = [n.find("a:name", ns).text for n in entry.findall("a:author", ns)]
            names = [n for n in names if n]
            abs_id = id_el.text.strip().replace("http://arxiv.org/abs/", "")
            abs_id = abs_id.replace("http://arxiv.org/pdf/", "").split("v")[0]
            link = f"https://arxiv.org/abs/{abs_id}"
            authors = ", ".join(names[:6]) + (" 等" if len(names) > 6 else "")
            best = (link, got_title, authors)
    if best_score < 0.45:
        return None
    return best


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--skip-arxiv", action="store_true")
    parser.add_argument("--sleep", type=float, default=3.0)
    args = parser.parse_args()

    ev = load_evidence()
    source = PAGE.read_text(encoding="utf-8")
    match = PATTERN.search(source)
    if not match:
        raise SystemExit("papers-json missing")
    papers = json.loads(match.group(2))

    from_ev = 0
    from_arxiv = 0
    skipped = 0

    for p in papers:
        if not needs_enrich(p):
            continue
        if apply_evidence(p, ev):
            from_ev += 1
            continue
        if args.skip_arxiv:
            skipped += 1
            continue
        title = (p.get("en") or p.get("zh") or "").strip()
        if not title or title == p.get("zh") and len(title) < 4:
            skipped += 1
            continue
        try:
            hit = arxiv_lookup(title, p.get("year"))
        except OSError as e:
            print("arxiv error", p["id"], e)
            skipped += 1
            time.sleep(args.sleep)
            continue
        time.sleep(args.sleep)
        if not hit:
            skipped += 1
            continue
        link, en, authors = hit
        p["link"] = link
        p["en"] = en
        p["authors"] = authors
        p["venue"] = "arXiv / 原始论文"
        from_arxiv += 1

    print(f"evidence: {from_ev}; arxiv: {from_arxiv}; skipped: {skipped}")
    if args.dry_run:
        return
    payload = json.dumps(papers, ensure_ascii=False, separators=(",", ":"))
    PAGE.write_text(source[: match.start(2)] + payload + source[match.end(2) :], encoding="utf-8")
    print(f"wrote {PAGE}")


if __name__ == "__main__":
    main()
