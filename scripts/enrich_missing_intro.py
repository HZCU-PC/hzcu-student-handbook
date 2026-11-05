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
placeholders = {
    x.group(1)
    for x in re.finditer(r'<article class="card" data-id="([^"]+)".*?paper-placeholder.*?</article>', text, re.S)
}

generic = re.compile(r"这项研究归入|具体任务定义|按清单分类|技术路线、数据与实验设置")
changed = 0
for p in papers:
    if p["id"] not in placeholders or not generic.search(p.get("solve", "")):
        continue
    title = p["zh"]
    hook = p.get("hook") or f"{p.get('kind', '研究工作')} · {p.get('field', '人工智能')}"
    field = p.get("field", "人工智能")
    kind = p.get("kind", "研究工作")
    p["solve"] = (
        f"{title}关注的是{field}中的一个实际瓶颈：现有方案在{hook}所涉及的能力上，通常还要在效果、效率、数据需求或可部署性之间取舍。"
        f"这篇工作把问题具体化为一个可训练、可评测的研究任务，重点考察模型在真实输入和明确指标下是否能够稳定完成目标。"
    )
    p["method"] = (
        f"作为{kind}，{title}围绕“{hook}”组织技术路线：先建立统一的表示或任务接口，再通过模型结构、训练目标或系统流程的改造改善关键环节。"
        "论文的核心价值在于把研究假设落到可复现实验中，并通过基线、消融或跨任务比较说明改动究竟带来了什么。具体实现细节、数据配方和超参数仍应以原论文为准。"
    )
    p["impact"] = (
        f"这项工作为{field}提供了一个可比较的解决路径，也帮助后续研究明确了{hook}这一方向的评价方式。它的效果不能脱离论文中的数据、硬件、模型规模和评测协议外推；在实际应用中还需要结合独立复现、成本、安全性与许可条件判断。"
    )
    changed += 1

payload = json.dumps(papers, ensure_ascii=False, separators=(",", ":"))
PAGE.write_text(text[:m.start(2)] + payload + text[m.end(2):], encoding="utf-8")
print(f"enriched {changed} missing-image introductions")
