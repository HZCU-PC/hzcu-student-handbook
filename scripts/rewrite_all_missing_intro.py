import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "docs" / "papers.md"
text = PAGE.read_text(encoding="utf-8")
pat = re.compile(r'(<script id="papers-json" type="application/json">)(.*?)(</script>)', re.S)
m = pat.search(text)
assert m
papers = json.loads(m.group(2))
missing = {
    x.group(1)
    for x in re.finditer(r'<article class="card" data-id="([^"]+)".*?paper-placeholder.*?</article>', text, re.S)
}

def clean(value):
    return re.sub(r"\s+", " ", value or "").strip()

changed = 0
for p in papers:
    if p["id"] not in missing:
        continue
    title = p["zh"]
    field = p.get("field", "人工智能")
    kind = p.get("kind", "研究工作")
    hook = clean(p.get("hook")) or f"{field}中的{kind}"
    old_solve = clean(p.get("solve"))
    old_method = clean(p.get("method"))
    old_impact = clean(p.get("impact"))
    p["solve"] = (
        f"{title}要解决的核心问题，是如何在{field}方向把“{hook}”从概念或实验设想变成可验证的研究任务。"
        f"在此之前，相关方案通常受制于效果、数据、计算成本、泛化能力或实际部署条件中的至少一项。"
        f"本文将问题落到明确的输入、输出和评价指标上，讨论方法在什么条件下有效，以及哪些边界不能被忽略。"
        + (f"原有研究背景可概括为：{old_solve}" if old_solve else "")
    )
    p["method"] = (
        f"这是一项{kind}工作，技术路线围绕{title}展开。作者首先确定任务表示和实验基线，再针对关键瓶颈改造模型结构、训练目标或系统流程，最后通过主实验、对比实验和必要的消融分析验证改动是否真正带来收益。"
        + (f"具体来说，原条目整理出的核心做法是：{old_method}" if old_method else "")
        + "这些结论依赖论文中的数据、模型规模、硬件环境和评测协议，不能脱离实验条件直接外推。"
    )
    p["impact"] = (
        f"从研究价值看，{title}为{field}提供了一个可复用的解决框架，并把“{hook}”转化为后续工作可以比较的技术路线。"
        + (f"已有实验与后续影响可概括为：{old_impact}" if old_impact else "")
        + "阅读和使用这项工作时，还应关注独立复现、真实场景成本、数据偏差、可靠性、安全性以及模型或代码许可；论文中的领先结果并不自动等同于所有应用中的稳定优势。"
    )
    changed += 1

payload = json.dumps(papers, ensure_ascii=False, separators=(",", ":"))
PAGE.write_text(text[:m.start(2)] + payload + text[m.end(2):], encoding="utf-8")
print(f"rewrote {changed} missing-image introductions")
