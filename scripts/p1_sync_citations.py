"""卡片角标与 JSON citations 对齐（每张卡只保留一个角标元素，绝不新增）。

历史坑（都是"审计报 0、页面仍错"的成因）：
  1. 旧版只认 <small>，对 39 张有图卡片是「插入 <small>」而不改可见 <span class="cite">；
  2. 精确匹配 class="cite" 漏掉 12 张 class="cite hot"；
  3. 角标值形如 "<1千"，含裸 < 让 [^<]* 失配，61 张占位卡被当成"无角标"又被插入一个
     <small> —— 于是 135 张卡片同时有两个 <small>，渲染成 "<1千<1千"。

本版规则（normalize 成恰好一个角标）：
  * shot 内有 span.cite → 改它的文本，删除 shot 内所有 <small>；
  * shot 内只有 <small> → 改第一个的文本，删除其余；
  * 两者都没有 → 不动（不新增元素，避免重演插入事故）；
  * 角标文本做 HTML 转义（"<1千" → "&lt;1千"），避免与 minify_html 打架。

用法：
    python scripts/p1_sync_citations.py --check   # 只报告，不写文件
    python scripts/p1_sync_citations.py           # 写回 docs/papers.md（需持锁）
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "docs" / "papers.md"

json_pat = re.compile(
    r'(<script id="papers-json" type="application/json">)(.*?)(</script>)', re.S
)
# (.*?) 而不是 [^<]*：角标可能是 "<1千" 这种以 < 开头的值。
CITE_RE = re.compile(r'(<span class="cite[^"]*">)(.*?)(</span>)')
SMALL_RE = re.compile(r"<small>(.*?)</small>")
CARD_RE = re.compile(
    r'(<article class="card" data-id="(WB-[^"]+)")([^>]*>)(.*?)(</article>)', re.S
)
BODY_SPLIT = '<div class="cbody"'


def esc_badge(s: str) -> str:
    """角标文本写进 HTML 前转义：形如 "<1千" 的值里那个裸 < 在 minify_html 下是隐患。"""
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def main() -> None:
    text = PAGE.read_text(encoding="utf-8")
    jm = json_pat.search(text)
    if not jm:
        raise SystemExit(f"papers-json 不存在：{PAGE}")
    cit = {p["id"]: (p.get("citations") or "").strip() for p in json.loads(jm.group(2))}

    fixed_cite, fixed_small, no_badge, dropped = [], [], [], 0

    def fix_card(m: re.Match) -> str:
        nonlocal dropped
        head_open, pid, tail_open, body, close = m.groups()
        want = cit.get(pid, "")
        if not want:
            return m.group(0)
        want_html = esc_badge(want)
        shot, sep, rest = body.partition(BODY_SPLIT)

        c = CITE_RE.search(shot)
        smalls = SMALL_RE.findall(shot)
        if not c and not smalls:
            no_badge.append(pid)
            return m.group(0)

        if c:
            new_shot = CITE_RE.sub(
                lambda mm: mm.group(1) + want_html + mm.group(3), shot, count=1
            )
            stray = len(SMALL_RE.findall(new_shot))
            if stray:
                new_shot = SMALL_RE.sub("", new_shot)
                dropped += stray
            target = fixed_cite
        else:
            first = SMALL_RE.search(shot)
            new_shot = (
                shot[: first.start()]
                + f"<small>{want_html}</small>"
                + SMALL_RE.sub("", shot[first.end():])
            )
            extra = len(smalls) - 1
            if extra > 0:
                dropped += extra
            target = fixed_small

        if new_shot == shot:
            return m.group(0)
        target.append(pid)
        return head_open + tail_open + new_shot + sep + rest + close

    new_text = CARD_RE.sub(fix_card, text)
    print(
        f"span.cite 改写 {len(fixed_cite)} 张；<small> 改写 {len(fixed_small)} 张；"
        f"删除重复角标 {dropped} 个；无角标跳过 {len(no_badge)} 张"
    )
    if "--check" in sys.argv:
        print("（--check：未写入）")
        return
    if new_text != text:
        PAGE.write_text(new_text, encoding="utf-8")
        print(f"已写入 {PAGE}")
    else:
        print("无需改动")


if __name__ == "__main__":
    main()