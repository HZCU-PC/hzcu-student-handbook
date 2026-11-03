"""Regenerate the paper card HTML from the embedded papers JSON.

The JSON block is read-only for this tool. Existing ``.shot`` inner HTML is
preserved by paper id so screenshots are never decoded or rewritten.
"""
from __future__ import annotations

import argparse
import html
import json
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "docs" / "papers.md"
BACKUP_DIR = ROOT / "backups"
BACKUP_PATH = BACKUP_DIR / "papers.md.gen.bak"
JSON_RE = re.compile(
    r'(<script id="papers-json" type="application/json">)(.*?)(</script>)', re.S
)
GRID_RE = re.compile(
    r'(?P<open><div[^>]*\bid="grid"[^>]*>)'
    r'(?P<body>.*?)'
    r'(?P<close></div>\s*(?=<div class="empty" id="empty"))',
    re.S,
)
CARD_RE = re.compile(
    r'<article class="card" data-id="(?P<id>[^"]+)".*?</article>', re.S
)
SHOT_RE = re.compile(r'<div class="shot(?: [^"]+)?">(?P<body>.*?)</div>', re.S)
FIELD_STYLE_RE = re.compile(
    r'<article[^>]*data-field="(?P<field>[^"]+)".*?'
    r'<span class="tag t-field"(?P<attrs>[^>]*)>', re.S
)
CITE_RE = re.compile(r'<span class="cite[^>]*>.*?</span>', re.S)
SMALL_RE = re.compile(r'<small>.*?</small>', re.S)


def esc(value: object) -> str:
    return html.escape(str(value if value is not None else ""), quote=True)


def esc_badge(value: object) -> str:
    return html.escape(str(value or ""), quote=False)


def load(text: str) -> tuple[list[dict], re.Match[str], re.Match[str]]:
    jm = JSON_RE.search(text)
    if not jm:
        raise SystemExit("papers-json block not found")
    gm = GRID_RE.search(text)
    if not gm:
        raise SystemExit("#grid block not found")
    return json.loads(jm.group(2)), jm, gm


def collect_shots(grid_body: str) -> dict[str, str]:
    shots: dict[str, str] = {}
    for card in CARD_RE.finditer(grid_body):
        sm = SHOT_RE.search(card.group(0))
        if sm:
            shots[card.group("id")] = sm.group("body")
    return shots


def collect_field_styles(text: str) -> dict[str, str]:
    return {
        m.group("field"): m.group("attrs")
        for m in FIELD_STYLE_RE.finditer(text)
    }


def badge(paper: dict) -> str:
    citations = esc_badge(paper.get("citations", ""))
    return citations


def cite_span(paper: dict) -> str:
    cls = "cite hot" if (paper.get("crank") or 0) >= 4 else "cite"
    return f'<span class="{cls}">{badge(paper)}</span>'


def shot_html(paper: dict, shots: dict[str, str]) -> str:
    pid = paper["id"]
    preserved = shots.get(pid)
    if preserved is not None:
        # Normalize only the badge text; preserve the image/base64 bytes and
        # all other shot markup exactly as it appeared in the source.
        if "shotimg" in preserved:
            if CITE_RE.search(preserved):
                preserved = CITE_RE.sub(cite_span(paper), preserved, count=1)
                preserved = SMALL_RE.sub("", preserved)
            elif SMALL_RE.search(preserved):
                preserved = SMALL_RE.sub(
                    f'<small>{badge(paper)}</small>', preserved, count=1
                )
            return f'<div class="shot">{preserved}</div>'
        # Existing placeholders are regenerated from JSON so they cannot
        # retain a stale or duplicate badge.
    suffix = paper.get("number") or pid.removeprefix("WB-")
    return (
        f'<div class="shot paper-placeholder"><span>{esc(suffix)}</span>'
        f'<small>{badge(paper)}</small></div>'
    )


def render_card(paper: dict, shots: dict[str, str], field_styles: dict[str, str]) -> str:
    field = str(paper.get("field") or "")
    kind = str(paper.get("kind") or "")
    country = str(paper.get("country") or "")
    year = paper.get("year") or ""
    hook = paper.get("hook") or (f"{field} · {kind}" if field or kind else "")
    style = field_styles.get(field, ' style="background:#ECEFF1;color:#546E7A"')
    tags = (
        f'<span class="tag t-field"{style}>{esc(field)}</span>'
        f'<span class="tag">{esc(kind)}</span>'
        f'<span class="tag">{esc(country)}</span>'
        f'<span class="tag tag-y">{esc(year)}</span>'
    )
    return (
        f'<article class="card" data-id="{esc(paper["id"])}" '
        f'data-field="{esc(field)}" data-kind="{esc(kind)}" '
        f'data-country="{esc(country)}" data-org="{esc(paper.get("org") or "")}" '
        f'data-year="{esc(year)}" tabindex="0" role="button" '
        f'aria-label="{esc(paper.get("zh") or "")}">'
        f'{shot_html(paper, shots)}<div class="cbody">\n'
        f'    <h3>{esc(paper.get("zh") or "")}</h3>'
        f'<p class="hook">{esc(hook)}</p><div class="tags">\n'
        f'      {tags}\n'
        f'    </div><div class="cmeta">{esc(paper.get("org") or "")}'
        f'<span class="dot">·</span>{esc(kind)}</div>\n  </div></article>'
    )


def regenerate(text: str) -> tuple[str, int, int]:
    papers, _, gm = load(text)
    shots = collect_shots(gm.group("body"))
    styles = collect_field_styles(text)
    cards = "\n".join(render_card(p, shots, styles) for p in papers)
    new_text = text[: gm.start("body")] + "\n" + cards + "\n" + text[gm.end("body") :]
    return new_text, len(papers), len(shots)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="report changes without writing")
    args = parser.parse_args()
    original = PAGE.read_text(encoding="utf-8")
    generated, count, preserved = regenerate(original)
    changed = generated != original
    print(f"cards from JSON: {count}; preserved shots: {preserved}; changed: {changed}")
    if args.check:
        print("--check: no files written")
        return
    if changed:
        BACKUP_DIR.mkdir(parents=True, exist_ok=True)
        shutil.copy2(PAGE, BACKUP_PATH)
        PAGE.write_text(generated, encoding="utf-8")
        print(f"wrote {PAGE}; backup {BACKUP_PATH}")
    else:
        print("no changes needed")


if __name__ == "__main__":
    main()
