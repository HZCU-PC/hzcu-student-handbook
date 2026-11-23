"""Final hook dedupe: remaining template-style card titles."""
import json
import re
from pathlib import Path

PAGE = Path(__file__).resolve().parents[1] / "docs" / "papers.md"
PATTERN = re.compile(
    r'(<script id="papers-json" type="application/json">)(.*?)(</script>)', re.S
)

PATCHES = {
    "WB-B14": ("基座模型 · 视觉", "图文对比预训练实现开放词汇 CLIP"),
    "WB-C07": ("训练与优化 · 语言", "排列语言建模的 XLNet 预训练"),
    "WB-C10": ("应用系统 · 语言", "弱监督大规模训练的 Whisper 语音识别"),
    "WB-D03": ("训练与优化 · 决策", "裁剪目标稳定策略更新的 PPO"),
    "WB-D04": ("应用系统 · 决策", "自我对弈强化学习的 AlphaZero"),
    "WB-D05": ("训练与优化 · 决策", "最大熵 off-policy 的 Soft Actor-Critic"),
}


def main() -> None:
    source = PAGE.read_text(encoding="utf-8")
    match = PATTERN.search(source)
    if not match:
        raise SystemExit("papers-json block not found")
    papers = json.loads(match.group(2))
    by_id = {p["id"]: p for p in papers}
    stale = []
    for pid, (old, new) in PATCHES.items():
        cur = (by_id[pid].get("hook") or "").strip()
        if cur != old:
            stale.append(f"{pid}({cur!r})")
    if stale:
        raise SystemExit(f"Refusing: hook not as expected: {', '.join(stale)}")
    for pid, (_, new) in PATCHES.items():
        by_id[pid]["hook"] = new
    payload = json.dumps(papers, ensure_ascii=False, separators=(",", ":"))
    PAGE.write_text(source[: match.start(2)] + payload + source[match.end(2) :], encoding="utf-8")
    print(f"hook dedupe-2 applied: {len(PATCHES)} patches")


if __name__ == "__main__":
    main()
