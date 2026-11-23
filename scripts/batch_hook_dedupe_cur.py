"""Deduplicate card-facing hooks that share generic kind · field labels."""
import json
import re
from pathlib import Path

PAGE = Path(__file__).resolve().parents[1] / "docs" / "papers.md"
PATTERN = re.compile(
    r'(<script id="papers-json" type="application/json">)(.*?)(</script>)', re.S
)

# id -> (required_current_hook, new_hook)
PATCHES = {
    # 9× 基座模型 · 语言
    "WB-A10": ("基座模型 · 语言", "双向 Transformer 预训练与句子表示"),
    "WB-A11": ("基座模型 · 语言", "语言建模预训练与零样本任务迁移"),
    "WB-A12": ("基座模型 · 语言", "少样本提示执行新任务的大模型"),
    "WB-A16": ("基座模型 · 语言", "千亿级中文自回归语言模型 PanGu-α"),
    "WB-A17": ("基座模型 · 语言", "知识增强的统一预训练 ERNIE 3.0"),
    "WB-A18": ("基座模型 · 语言", "超大规模中文多模态 WuDao 2.0"),
    "WB-A21": ("基座模型 · 语言", "Pathways 大规模语言模型 PaLM"),
    "WB-A51": ("基座模型 · 语言", "通用与推理模式统一的 Qwen3"),
    "WB-H08": ("基座模型 · 语言", "多语言稠密与稀疏检索 BGE-M3"),
    # 14× 数据与基准 · 语言
    "WB-I02": ("数据与基准 · 语言", "多任务自然语言理解基准 GLUE"),
    "WB-I03": ("数据与基准 · 语言", "更高难度的语言理解 SuperGLUE"),
    "WB-I04": ("数据与基准 · 语言", "57 科多项选择知识评测 MMLU"),
    "WB-I05": ("数据与基准 · 语言", "函数级 Python 代码生成 HumanEval"),
    "WB-I06": ("数据与基准 · 语言", "小学数学文字题基准 GSM8K"),
    "WB-I07": ("数据与基准 · 语言", "统一场景的语言模型评测 HELM"),
    "WB-I08": ("数据与基准 · 语言", "协作式大规模能力探针 BIG-bench"),
    "WB-I09": ("数据与基准 · 语言", "中文多学科知识评测 C-Eval"),
    "WB-I10": ("数据与基准 · 语言", "中文大规模多学科 CMMLU"),
    "WB-I11": ("数据与基准 · 语言", "面向 AGI 的考试题集 AGIEval"),
    "WB-I12": ("数据与基准 · 语言", "人类偏好的对话模型竞技场"),
    "WB-I13": ("数据与基准 · 语言", "真实 Issue 修代码 SWE-bench"),
    "WB-I14": ("数据与基准 · 语言", "竞赛级数学证明题 MATH"),
    "WB-J03": ("数据与基准 · 语言", "教学 Copilot 场景评测框架"),
    # 6× 应用系统 · 科学
    "WB-F02": ("应用系统 · 科学", "三轨道网络快速蛋白结构 RoseTTAFold"),
    "WB-F05": ("应用系统 · 科学", "给定骨架设计序列的 ProteinMPNN"),
    "WB-F09": ("应用系统 · 科学", "错义突变致病性预测 AlphaMissense"),
    "WB-F10": ("应用系统 · 科学", "全球中期天气预报 Pangu-Weather"),
    "WB-F15": ("应用系统 · 科学", "化学任务工具增强代理 ChemCrow"),
    "WB-F16": ("应用系统 · 科学", "多分子复合物结构 AlphaFold 3"),
    # 3× 新架构 · 视觉
    "WB-B03": ("新架构 · 视觉", "深层 3×3 卷积堆叠的 VGG"),
    "WB-B06": ("新架构 · 视觉", "RPN 与检测器联合的 Faster R-CNN"),
    "WB-B15": ("新架构 · 视觉", "层次化窗口注意力的 Swin Transformer"),
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
        if pid not in by_id:
            raise SystemExit(f"Unknown id: {pid}")
        cur = (by_id[pid].get("hook") or "").strip()
        if cur != old:
            stale.append(f"{pid}({cur!r})")
    if stale:
        raise SystemExit(f"Refusing: hook not as expected: {', '.join(stale)}")
    for pid, (_, new) in PATCHES.items():
        by_id[pid]["hook"] = new
    payload = json.dumps(papers, ensure_ascii=False, separators=(",", ":"))
    PAGE.write_text(source[: match.start(2)] + payload + source[match.end(2) :], encoding="utf-8")
    print(f"hook dedupe applied: {len(PATCHES)} patches")


if __name__ == "__main__":
    main()
