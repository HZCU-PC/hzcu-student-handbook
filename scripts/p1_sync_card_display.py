"""从 #papers-json 同步卡片 h3 / aria-label / hook（按 article 块）。"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "docs" / "papers.md"
text = PAGE.read_text(encoding="utf-8")
jm = re.search(
    r'<script id="papers-json" type="application/json">(.*?)</script>', text, re.S
)
DATA = {p["id"]: p for p in json.loads(jm.group(1))}

ONLY = {
    "WB-A22", "WB-A24", "WB-A25", "WB-A26", "WB-A28", "WB-A32", "WB-A33",
    "WB-A34", "WB-A36", "WB-A39", "WB-A40", "WB-A47", "WB-B01", "WB-B04",
    "WB-A50", "WB-A52",
}

changed = 0


def sync_article(m: re.Match) -> str:
    global changed
    pid = m.group(2)
    if ONLY and pid not in ONLY:
        return m.group(0)
    p = DATA.get(pid)
    if not p:
        return m.group(0)
    block = m.group(0)
    zh = (p.get("zh") or "").replace('"', "&quot;")
    hook = p.get("hook") or ""
    new_block = block
    new_block2 = re.sub(
        r'aria-label="[^"]*"',
        f'aria-label="{zh}"',
        new_block,
        count=1,
    )
    if new_block2 != new_block:
        changed += 1
        new_block = new_block2
    new_block = re.sub(r"<h3>[^<]*</h3>", f"<h3>{p.get('zh', '')}</h3>", new_block, count=1)
    if hook:
        new_block = re.sub(
            r'<p class="hook">[^<]*</p>',
            f'<p class="hook">{hook}</p>',
            new_block,
            count=1,
        )
    return new_block


ART = re.compile(
    r'(<article class="card" data-id="(WB-[^"]+)"[^>]*>.*?</article>)', re.S
)
new_text = ART.sub(sync_article, text)

if new_text != text:
    PAGE.write_text(new_text, encoding="utf-8")
print("articles touched:", changed, "of scope", len(ONLY))
