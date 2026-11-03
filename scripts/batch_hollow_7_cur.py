"""Replace workbook placeholder prose for 7 entries missed by template batches."""
import json
import re
from pathlib import Path

PAGE = Path(__file__).resolve().parents[1] / "docs" / "papers.md"
PATTERN = re.compile(
    r'(<script id="papers-json" type="application/json">)(.*?)(</script>)', re.S
)

PLACEHOLDER_MARKERS = (
    "请以原论文为准",
    "所对应的问题",
    "按清单分类",
)

EXPECTED = frozenset(
    "WB-A41 WB-A48 WB-A53 WB-B21 WB-C04 WB-D16 WB-G01".split()
)


def _is_placeholder(p: dict) -> bool:
    blob = " ".join((p.get(k) or "") for k in ("solve", "method", "impact", "hook"))
    return any(m in blob for m in PLACEHOLDER_MARKERS)


CONTENT = {
    "WB-A41": {
        "solve": "混合专家模型可以在不线性增加每次推理计算的前提下扩大参数量，但路由与负载均衡很难做好。DeepSeek-MoE 针对细粒度专家划分与共享专家组合，报告一套可训练的大规模 MoE 语言模型方案。",
        "method": "架构把前馈层拆成大量细粒度专家，并保留共享专家处理公共模式；路由网络为每个 token 选择少量专家。论文描述训练时的负载均衡与通信策略，并在语言建模与公开基准上报告结果。",
        "impact": "工作提供了开源 MoE 设计与训练细节，便于与稠密模型对照。作者报告的吞吐与基准分数依赖硬件与路由配置；MoE 的实际服务成本仍受专家激活比例和并行实现影响。",
        "hook": "细粒度专家加共享专家的大 MoE 语言模型",
    },
    "WB-A48": {
        "solve": "长上下文与复杂推理任务要求模型在预训练之外继续强化多步思考能力。Kimi k1.5 技术报告说明月之暗面如何在近期版本中扩展上下文并强化推理相关训练。",
        "method": "报告概述数据配比、长文本处理、监督微调与强化学习等后训练环节，并在数学、代码与多模态等任务上给出评测。具体配方与算力数字应以发布方文档为准，不同产品接口能力并不完全一致。",
        "impact": "报告为外界提供了 Kimi 系列能力演进的公开说明。榜单成绩属于作者测试设置；API 版本、提示模板与安全策略都会改变可用表现，独立复现受权重与数据限制。",
        "hook": "Kimi k1.5 的长上下文与推理后训练",
    },
    "WB-A53": {
        "solve": "开放基座模型需要在能力、推理成本与部署形态之间取舍。GLM-4.5 是智谱 AI 报告的新一代语言模型系列，覆盖不同规模与使用场景。",
        "method": "技术报告介绍模型规模划分、预训练语料与后训练流程，并对标 contemporaneous 基座在多项基准上的表现。工具调用、代码等能力是否开放取决于具体型号与发布渠道。",
        "impact": "报告集中呈现智谱对 GLM 路线的迭代。对外数字应标注为官方评测；权重许可与商用条款决定第三方能否验证，同一品牌下不同 SKU 能力差异较大。",
        "hook": "智谱 GLM-4.5 多规模基座系列",
    },
    "WB-B21": {
        "solve": "神经辐射场能合成高质量新视角，但训练和渲染往往太慢，难以实时交互。3D Gaussian Splatting 用显式三维高斯表示场景，以可微 splatting 追求实时渲染与高质量兼顾。",
        "method": "从稀疏点云初始化各向异性高斯，优化位置、协方差、不透明度和颜色；可微 rasterizer 将高斯投影到图像平面，并通过自适应增删高斯细化几何。论文在标准新视角合成数据集上报告 PSNR 与速度。",
        "impact": "该方法推动了实时新视角渲染与后续编辑工具链。效果受拍摄覆盖与校准影响；显式表示便于编辑，但存储与极端视角仍可能不如最新隐式方法稳定。",
        "hook": "显式高斯 splat 实现实时新视角合成",
    },
    "WB-C04": {
        "solve": "传统短语统计机器翻译难以建模长距离依赖，且在大量语料上扩展效率有限。Google 神经机器翻译（GNMT）尝试用端到端深度网络统一翻译流程。",
        "method": "系统采用带残差连接的深层 LSTM 编码器—解码器，并在层间引入注意力；词表使用 wordpiece 处理开放词汇。论文在多种语言对上训练并报告 BLEU，并讨论在生产集群上的部署经验。",
        "impact": "GNMT 在多个难语言对上显著超过当时短语系统，证明神经网络翻译可规模化上线。后续 Transformer 进一步取代 LSTM 架构，但 GNMT 是工业神经 MT 的关键过渡节点。",
        "hook": "深层 LSTM 注意力端到端神经机器翻译",
    },
    "WB-D16": {
        "solve": "复杂数学与逻辑题常需要多步推导，单次短回答的大模型容易出错。OpenAI o1 系列强调在给出可见答案前分配额外计算做内部推理。",
        "method": "训练在大规模预训练基础上加入面向推理任务的强化学习；推理阶段模型生成长链中间步骤后再输出最终回答。公开材料以产品说明与部分基准为主，完整数据与奖励设计未完全披露。",
        "impact": "官方报告在竞赛数学与编程等任务上相对前代有提升，但延迟与调用成本随推理长度上升。行为受 API 策略与安全过滤影响，外部难以复现同等训练条件。",
        "hook": "为难题预留长推理再作答的 o 系列",
    },
    "WB-G01": {
        "solve": "当 Transformer 语言模型超过单卡显存时，需要在保持数学等价的前提下切分参数与激活。Megatron-LM 系统化张量并行与流水线并行，用于训练超大模型。",
        "method": "张量并行在 attention 与 MLP 矩阵上乘以分片布局；流水线并行把层段落到不同设备并按 microbatch 调度；实现与混合精度及数据并行组合。论文报告在 GPT 类模型上的扩展效率与收敛行为。",
        "impact": "Megatron 式并行成为许多大模型训练栈的基础模块。实际加速比依赖 NVLink 等互联与 batch 设置；后续框架在调度与内存上继续改进，但核心切分思想仍被广泛沿用。",
        "hook": "张量并行与流水线并行训练超大 Transformer",
    },
}


def main() -> None:
    if set(CONTENT) != EXPECTED:
        raise SystemExit("CONTENT ids must match EXPECTED hollow set")
    source = PAGE.read_text(encoding="utf-8")
    match = PATTERN.search(source)
    if not match:
        raise SystemExit("papers-json block not found")
    papers = json.loads(match.group(2))
    by_id = {p["id"]: p for p in papers}
    missing = sorted(set(CONTENT) - set(by_id))
    if missing:
        raise SystemExit(f"Unknown paper ids: {missing}")
    not_hollow = sorted(pid for pid in CONTENT if not _is_placeholder(by_id[pid]))
    if not_hollow:
        raise SystemExit(f"Refusing to overwrite non-placeholder entries: {not_hollow}")
    for pid, fields in CONTENT.items():
        by_id[pid].update(fields)
    payload = json.dumps(papers, ensure_ascii=False, separators=(",", ":"))
    PAGE.write_text(source[: match.start(2)] + payload + source[match.end(2) :], encoding="utf-8")
    print(f"hollow-7 applied: {len(CONTENT)} JSON patches")


if __name__ == "__main__":
    main()
