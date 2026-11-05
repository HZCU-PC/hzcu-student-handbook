"""P1 数据债审计（只读 stdout，不改文件）。"""
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "docs" / "papers.md"
text = PAGE.read_text(encoding="utf-8")
pat = re.compile(
    r'(<script id="papers-json" type="application/json">)(.*?)(</script>)', re.S
)
m = pat.search(text)
assert m, "papers-json missing"
DATA = json.loads(m.group(2))
BY = {p["id"]: p for p in DATA}

card_pat = re.compile(
    r'<article class="card" data-id="(WB-[^"]+)"',
)
cards = card_pat.findall(text)

ART = re.compile(
    r'<article class="card" data-id="(WB-[^"]+)"[^>]*>(.*?)</article>', re.S
)
# 卡片角标：优先 span.cite，其次 <small>。
# 注意两点（都曾造成"审计报 0 但其实没修"）：
#  1. class 可能是 "cite" 或 "cite hot" —— 精确匹配 "cite" 会让 hot 卡整类隐形；
#  2. 角标文本里有 "<1千" 这种以 < 开头的值，用 [^<]* 会直接失配（5 张卡曾因此隐形）。
CITE_RE = re.compile(r'<span class="cite[^"]*">(.*?)</span>')
SMALL_RE = re.compile(r"<small>(.*?)</small>")


def _plain(s: str) -> str:
    """HTML 实体还原，便于与 JSON 比较。"""
    return (s.replace("&lt;", "<").replace("&gt;", ">").replace("&amp;", "&")).strip()


badge_by_id = {}
dual_badge = []
multi_badge = []
for pid, body in ART.findall(text):
    c = CITE_RE.search(body)
    smalls = SMALL_RE.findall(body)
    sm = SMALL_RE.search(body)
    if c:
        badge_by_id[pid] = _plain(c.group(1))
        if sm:
            dual_badge.append(pid)
    elif sm:
        badge_by_id[pid] = _plain(sm.group(1))
    # 一个卡片应当只有一个角标元素：cite+small 或 两个 small 都算重复显示
    if len(smalls) + (1 if c else 0) > 1:
        multi_badge.append(pid)

tpl_solve = "核心问题，是如何"
tpl_hook = re.compile(r"^[^·]+ · [^·]+$")  # 字段 · 类型
THIN_MIN = 60
PLACEHOLDER_MARKERS = (
    "请以原论文为准",
    "所对应的问题",
    "按清单分类",
)


def _thin_fields(p: dict) -> list[str]:
    short = []
    for key in ("solve", "method", "impact"):
        if len((p.get(key) or "").strip()) < THIN_MIN:
            short.append(key)
    return short


def _placeholder_prose(p: dict) -> bool:
    blob = " ".join((p.get(k) or "") for k in ("solve", "method", "impact", "hook"))
    return any(m in blob for m in PLACEHOLDER_MARKERS)


thin_ids = sorted(p["id"] for p in DATA if _thin_fields(p))
placeholder_ids = sorted(p["id"] for p in DATA if _placeholder_prose(p))

stats = {
    "papers": len(DATA),
    "cards": len(cards),
    "template_solve": sum(1 for p in DATA if tpl_solve in (p.get("solve") or "")),
    "template_hook": sum(
        1
        for p in DATA
        if tpl_hook.match((p.get("hook") or "").strip())
    ),
    "placeholder_authors": sum(
        1 for p in DATA if "作者信息见原论文" in (p.get("authors") or "")
    ),
    "arxiv_search_link": sum(
        1
        for p in DATA
        if "arxiv.org/search" in (p.get("link") or "").lower()
    ),
    "citation_mismatch": 0,
    "dual_badge_cards": len(dual_badge),
    "duplicate_badge_cards": len(multi_badge),
    "thin_content": len(thin_ids),
    "thin_content_ids": thin_ids,
    "placeholder_prose": len(placeholder_ids),
    "placeholder_prose_ids": placeholder_ids,
    "card_ids_missing_json": [],
    "json_ids_missing_card": [],
}

card_ids = set(cards)
json_ids = set(BY)
stats["card_ids_missing_json"] = sorted(card_ids - json_ids)
stats["json_ids_missing_card"] = sorted(json_ids - card_ids)

for cid in cards:
    p = BY.get(cid)
    if not p:
        continue
    vis = (badge_by_id.get(cid) or "").strip()
    cit = (p.get("citations") or "").strip()
    if cit and vis and cit != vis:
        stats["citation_mismatch"] += 1

zh = Counter(p["zh"] for p in DATA)
stats["duplicate_zh"] = {k: v for k, v in zh.items() if v > 1}

hook_labels = Counter((p.get("hook") or "").strip() for p in DATA if (p.get("hook") or "").strip())
stats["duplicate_hook_groups"] = sum(1 for c in hook_labels.values() if c > 1)
stats["max_hook_collision"] = max(hook_labels.values()) if hook_labels else 0

if __name__ == "__main__":
    import sys

    print(json.dumps(stats, ensure_ascii=False, indent=2))
    if "--mismatch" in sys.argv:
        for cid in cards:
            p = BY.get(cid)
            if not p:
                continue
            vis = (badge_by_id.get(cid) or "").strip()
            cit = (p.get("citations") or "").strip()
            if cit and vis and cit != vis:
                print(cid, vis, "->", cit)
    if "--dual" in sys.argv:
        print("dual badge:", " ".join(dual_badge))
    if "--dup" in sys.argv:
        print("duplicate badge:", " ".join(multi_badge))
    if "--thin" in sys.argv:
        for pid in thin_ids:
            print(pid, _thin_fields(BY[pid]))
    if "--placeholder" in sys.argv:
        print("placeholder prose:", " ".join(placeholder_ids))
