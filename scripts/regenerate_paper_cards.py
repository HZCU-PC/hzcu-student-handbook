"""Regenerate the paper card HTML from the embedded papers JSON.

The JSON block is read-only for this tool. Existing inline ``shotimg`` (base64) is
preserved by paper id. JPEG first-page captures in ``docs/assets/paper-thumbs/``
take precedence over SVG placeholders when regenerating.
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
THUMB_DIR = ROOT / "docs" / "assets" / "paper-thumbs"
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


def file_shotimg_inner(paper: dict) -> str | None:
    pid = paper["id"]
    path = THUMB_DIR / f"{pid}.jpg"
    if not path.is_file():
        return None
    alt = esc(paper.get("zh") or "论文第一页")
    src = esc(f"../assets/paper-thumbs/{pid}.jpg")
    return (
        f'<img class="shotimg" src="{src}" alt="{alt}" '
        f'loading="lazy" decoding="async">'
    )


def shot_html(paper: dict, shots: dict[str, str]) -> str:
    pid = paper["id"]
    preserved = shots.get(pid)
    if preserved is not None:
        # Normalize only the badge text; preserve the image/base64 bytes and
        # all other shot markup exactly as it appeared in the source.
        if "shotimg" in preserved:
            if "data:image" in preserved:
                if CITE_RE.search(preserved):
                    preserved = CITE_RE.sub(cite_span(paper), preserved, count=1)
                    preserved = SMALL_RE.sub("", preserved)
                elif SMALL_RE.search(preserved):
                    preserved = SMALL_RE.sub(
                        f'<small>{badge(paper)}</small>', preserved, count=1
                    )
                return f'<div class="shot">{preserved}</div>'
            file_img = file_shotimg_inner(paper)
            if file_img:
                return f'<div class="shot">{file_img}{cite_span(paper)}</div>'
    file_img = file_shotimg_inner(paper)
    if file_img:
        return f'<div class="shot">{file_img}{cite_span(paper)}</div>'
    if preserved is not None and "thumb-svg" in preserved:
        body = CITE_RE.sub("", preserved)
        body = SMALL_RE.sub("", body)
        return f'<div class="shot">{body.strip()}{cite_span(paper)}</div>'
    return f'<div class="shot">{svg_thumb_inner(paper)}{cite_span(paper)}</div>'


def _chunks(text: str, size: int, max_lines: int = 2) -> list[str]:
    text = (text or "").strip()
    if not text:
        return [""]
    out = []
    for i in range(0, min(len(text), size * max_lines), size):
        out.append(text[i : i + size])
    return out or [""]


def svg_thumb_inner(paper: dict) -> str:
    """Paper-style SVG preview (matches papers-workbench.css .thumb-svg)."""
    accent = esc(paper.get("color") or "#546E7A")
    venue = esc((paper.get("venue") or "Paper")[:38])
    yr = esc(str(paper.get("year") or ""))
    title_src = (paper.get("en") or paper.get("zh") or "").strip()
    if title_src == (paper.get("zh") or "").strip() and len(title_src) > 40:
        title_src = title_src[:40]
    lines = _chunks(title_src, 34, 2)
    y_title = 72
    title_nodes = []
    for line in lines:
        title_nodes.append(
            f'<text class="p-title" x="24" y="{y_title}">{esc(line)}</text>'
        )
        y_title += 15
    zh = esc((paper.get("zh") or "")[:22])
    authors = (paper.get("authors") or "").strip()
    if "作者信息见原论文" in authors:
        authors = (paper.get("org") or "")[:48]
    au = esc(authors[:58])
    y_meta = y_title + 4
    fig_y = y_meta + 22
    bars = []
    for i, w in enumerate((210, 235, 185, 220, 165)):
        bars.append(
            f'<rect class="p-bar" x="24" y="{fig_y + 128 + i * 9}" '
            f'width="{w}" height="5" rx="1"/>'
        )
    return (
        '<svg class="thumb-svg" viewBox="0 0 300 424" xmlns="http://www.w3.org/2000/svg" '
        'role="img" aria-hidden="true">'
        '<rect class="p-bg" width="300" height="424"/>'
        '<line class="p-rule" x1="24" y1="44" x2="276" y2="44"/>'
        f'<text class="p-venue" x="24" y="34" fill="{accent}">{venue}</text>'
        f'<text class="p-yr" x="276" y="34" text-anchor="end">{yr}</text>'
        + "".join(title_nodes)
        + f'<text class="p-zh" x="24" y="{y_meta}">{zh}</text>'
        + f'<text class="p-au" x="24" y="{y_meta + 14}">{au}</text>'
        + f'<rect class="p-fig" x="24" y="{fig_y}" width="252" height="112" rx="3"/>'
        + "".join(bars)
        + "</svg>"
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
