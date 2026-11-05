# -*- coding: utf-8 -*-
"""
batch03_wkb_draft.py — WKB 批次草稿（P1-a 扩写 × 14 + P1-b 改名 × 2）

⚠️ 状态：**已由 CUR 于 2026-11-04 执行合并**（见 logs/2026-11-04-0002-cursor-p1-merge.md）。
   再次运行会覆盖 JSON；仅在有新 CONTENT/RENAME 时编辑后重跑。
   本脚本只写 JSON 区块（#papers-json），不改卡片 HTML；
   卡片 h3/aria-label/hook 展示位如需同步，由 CUR 另行处理。
"""
import json, re
from pathlib import Path

page = Path(__file__).resolve().parents[1] / 'docs' / 'papers.md'
text = page.read_text(encoding='utf-8')
pat = re.compile(r'(<script id="papers-json" type="application/json">)(.*?)(</script>)', re.S)
m = pat.search(text); assert m
papers = json.loads(m.group(2))

# ============ P1-a：14 篇 solve/method/impact/hook 扩写 ============
CONTENT = {
 'WB-A22': {  # InstructGPT (2022, OpenAI) — hook 已为非模板，保留
  'solve': 'GPT-3 这类模型的训练目标只是预测下一个词，与用户意图并不天然对齐：它可能不遵循指令、编造事实或生成有害内容。核心问题是如何让大模型按用户的真实意图行动，而不只是补全文本。',
  'method': '作者让约 40 人的标注团队编写示范回答并对模型输出按偏好排序：先用标注示范做监督微调（SFT），再用排序数据训练奖励模型，最后用 PPO 强化学习对 1.3B–175B 的 GPT-3 做对齐微调，并报告了标注一致性与质量控制流程。',
  'impact': '1.3B 的 InstructGPT 在人工偏好评价中优于 175B 的 GPT-3，证明对齐带来的有用性提升可以超过百倍参数扩张。SFT＋奖励模型＋PPO 的流水线随后成为 ChatGPT 等助手模型的标准范式。局限是奖励模型继承标注者偏好，存在偏见与“迎合标注”风险。',
 },
 'WB-A24': {  # LLaMA 2 (2023, Meta)
  'solve': '2023 年中，开放权重模型仍明显落后于闭源旗舰，且多数不允许商用；同时“聊天助手”版本如何在有用性与安全性之间取舍，业界缺少公开、可复现的完整方案。',
  'method': '发布 7B/13B/70B 三档预训练模型：2T token 训练、4K 上下文、70B 档使用分组查询注意力（GQA）。配套 Llama 2-Chat 给出完整对齐配方：SFT、人类偏好数据收集、拒绝采样加 PPO，并提出 Ghost Attention 维持多轮对话中的系统指令；论文同时公开红队测试与安全奖励模型细节。',
  'impact': 'Llama 2 是首个允许商用的开放权重旗舰，直接成为大量企业与研究者的微调基座；其安全与对齐章节成为后续开放模型的实践参考。但许可附带月活 7 亿的限制条款，“开放”程度此后被 Apache 2.0 系模型反超。',
  'hook': '首个可商用开放权重旗舰，公开完整 RLHF 配方',
 },
 'WB-A25': {  # Mistral 7B (2023)
  'solve': '能否只用 7B 参数达到甚至超过更大的开放模型，同时保持低推理成本与完全开源（Apache 2.0）？这挑战了“性能只能靠堆参数”的惯性。',
  'method': '采用分组查询注意力（GQA）加速推理，滑动窗口注意力（SWA，窗口 4096）配合滚动缓存与前缀分块处理长序列；论文未详细披露训练数据构成，只给出架构与评测结果。',
  'impact': '在论文报告的多项基准上超过 Llama 2 13B、部分指标接近 Llama 1 34B，数学与代码表现突出；它确立了“高质量小模型”路线并催生大量社区微调。结论基于论文口径，实际收益随任务与部署条件变化。',
  'hook': '7B 打赢 13B：GQA＋滑动窗口注意力',
 },
 'WB-A26': {  # GPT-4 (2023, OpenAI)
  'solve': '大模型的能力随规模提升的边界在哪里？如何在训练前预测大模型的表现，并把安全性纳入训练流程而非事后补丁？',
  'method': '技术报告刻意不公开架构与数据细节，重点放在三件事：支持文本与图像输入的多模态能力；用小型模型外推大模型性能的“可预测扩展”基础设施；以及基于规则的奖励模型（RBRM）等安全机制。评测覆盖人类考试与学术基准。',
  'impact': '报告 GPT-4 在模拟律师资格考试中进入前 10%（GPT-3.5 约为后 10%），多模态与可控性显著提升，支撑了 ChatGPT 的商用爆发。但因竞争与安全理由不公开参数、数据与训练方法，可复现性在顶级模型中最受争议。',
  'hook': '考试进前 10% 的多模态旗舰，技术细节保密',
 },
 'WB-A28': {  # Gemini (2023, Google DeepMind)
  'solve': '此前多模态系统多是把单模态模型拼接起来，能力与效率受限；问题是如何从头训练原生多模态模型，并用同一技术族覆盖从数据中心到手机的部署谱系。',
  'method': 'Gemini 从一开始就联合建模文本、图像、音频与视频，而非后期拼接；基于 Transformer 与 TPUv4/v5e 训练基础设施，分 Ultra/Pro/Nano 三档，Ultra 上下文 32K，并系统公开责任与安全评测。',
  'impact': '报告 Gemini Ultra 在 MMLU 达 90.0%，号称首个超过人类专家的模型，多模态基准大幅领先。但演示视频与评测口径（CoT 设置）曾引发争议，实际对比应参考后续独立评测。',
  'hook': '原生多模态模型家族：从手机到数据中心',
 },
 'WB-A32': {  # RWKV (2023) — hook 保留
  'solve': 'Transformer 的推理成本随序列长度增长，而传统 RNN 虽为线性复杂度却难以并行训练、容量受限。核心问题是能否兼得 Transformer 的并行训练与 RNN 的线性推理。',
  'method': '把线性注意力重新参数化：训练时写成可并行的形式，推理时退化为每层常数状态的 RNN。引入 time-mix 与 channel-mix 模块、位置相关衰减与特定初始化技巧；由开源社区主导迭代（RWKV-4，后续 5/6 代）。',
  'impact': '证明纯 RNN 路线可扩展到 14B 参数并接近同规模 Transformer，成为“后 Transformer 架构”探索的代表之一。在长上下文检索等任务上仍落后于注意力模型，收益依任务与实现而定。',
 },
 'WB-A33': {  # Llama 3 (2024, Meta)
  'solve': '开放权重模型与最强闭源模型之间仍有代差；问题是如何靠“数据质量＋训练规模”把开放模型推进到同一梯队，并公开完整训练配方。',
  'method': '以 15T token 高质量语料（数据清洗管线大幅升级）训练 8B/70B/405B 三档；405B 在 1.6 万块 H100 上训练，后训练采用 SFT＋拒绝采样＋DPO 多轮迭代。技术报告系统披露预训练、后训练与多模态扩展细节。',
  'impact': '405B 在多项基准上达到 GPT-4 级别，成为开放权重生态新基座；报告本身成为开放模型训练的事实参考。训练数据版权与许可条款仍是持续争议点。',
  'hook': '15T token 喂出的开放权重旗舰',
 },
 'WB-A34': {  # Mixtral 8x7B (2024) — hook 保留
  'solve': '如何在不增加单次推理计算量的前提下扩大模型容量？稀疏专家模型此前多停留在研究阶段，能否做成开放权重且可商用？',
  'method': '每层用路由器从 8 个前馈专家中选 2 个（top-2）：总参数约 47B、每 token 激活约 13B，支持 32K 上下文，以 Apache 2.0 完整开放权重。',
  'impact': '在论文报告口径下多数基准匹配或超过 Llama 2 70B 与 GPT-3.5，推理速度显著更快；确立稀疏 MoE 为开放模型主流路线。实际部署需加载全部专家参数，显存与路由均衡是主要约束。',
 },
 'WB-A36': {  # Qwen2 (2024)
  'solve': '开放模型需要覆盖从端侧到服务器的完整尺寸谱系，并在中英之外的多语言、代码与数学任务上追赶闭源模型——此前国产开放模型在多语言上存在明显短板。',
  'method': '发布 0.5B–72B 五档模型，全系列采用分组查询注意力；约 7T token 多语言语料预训练，支持 32K 上下文并配长上下文外推方案；不同尺寸采用差异化许可（部分 Apache 2.0）。',
  'impact': '72B 在官方口径下多项基准超过 Llama 3 70B；Qwen 系列成为中国开放模型生态主力，被大量二次微调与行业部署。各尺寸许可不同，商用前需逐档核对。',
  'hook': '全尺寸谱系＋多语言的国产开放主力',
 },
 'WB-A39': {  # DeepSeek-V2 (2024) — hook 保留
  'solve': '大模型推理的 KV 缓存与训练算力是规模化部署的两大瓶颈；问题是如何在不牺牲性能的前提下大幅压缩二者。',
  'method': '提出多头潜在注意力（MLA），把 KV 缓存压缩为低秩潜在向量；配合细粒度专家＋共享专家的 DeepSeekMoE。总参数 236B、每 token 激活 21B，用 8.1T token 训练。',
  'impact': '论文报告相对 DeepSeek 67B：训练成本省 42.5%、KV 缓存减 93%、生成吞吐提升 5.76 倍。MLA 被 V3/R1 沿用，成为高效推理的代表性设计；收益依赖论文的实现与硬件条件，独立复现规模有限。',
 },
 'WB-A40': {  # DeepSeek-V3 (2024)
  'solve': '开放模型能否以远低于巨头的训练算力达到顶级闭源模型水平？训练效率本身成为被研究的对象。',
  'method': '671B 总参数、37B 激活，沿用 MLA＋DeepSeekMoE，新增无辅助损失的负载均衡与多 token 预测（MTP）；全程 FP8 混合精度训练，完整训练仅 2.788M H800 GPU 小时。',
  'impact': '多项基准与 GPT-4o、Claude 3.5 Sonnet 同级，官方折算训练成本约 557.6 万美元（仅最终训练 run 的 GPU 时租口径，不含研究与试错）。它改变了“只有巨头能训前沿模型”的认知，但成本数字常被脱离口径引用，需谨慎解读。',
  'hook': '2.788M GPU 小时训出的前沿模型',
 },
 'WB-A47': {  # DeepSeek-R1 (2025) — hook 保留
  'solve': '推理能力是否必须依赖大量人工标注的监督推理数据？核心问题是：纯强化学习能否让模型自发涌现出长链推理与自我反思。',
  'method': '先在 DeepSeek-V3-Base 上直接用规则奖励的 GRPO 强化学习得到 R1-Zero——涌现出“aha moment”式自我反思但可读性差；R1 采用冷启动 SFT＋推理导向 RL＋拒绝采样＋全场景 SFT/RL 的多阶段流程修正可读性，并蒸馏出 1.5B–70B 系列。',
  'impact': '数学与代码推理达到 o1 级别（AIME、MATH 官方口径），开放权重引发全球复现潮；证明“RL 激励推理”路线可行，推动 2025 年推理模型竞赛。已知问题包括语言混杂、提示敏感与安全对齐不足。',
 },
 'WB-B01': {  # LeNet-5 (1998) — hook 保留
  'solve': '手写字符识别此前依赖手工特征提取加单独分类器，误差逐级累积、换任务就要重做特征。核心问题是能否用梯度反向传播端到端地训练整个识别系统。',
  'method': '提出卷积层与子采样层交替的 7 层网络 LeNet-5：局部感受野＋共享权重大幅减少参数，使网络可直接从像素学习特征；论文还给出图变换网络（GTN），把分割、识别、语言模型纳入统一的可微框架。',
  'impact': '在 MNIST 等任务上确立卷积网络范式，并被银行支票读数系统大规模商用部署；奠定“以学习取代手工特征”的深度学习路线。受当时算力与数据规模限制，其路线十余年后再由 AlexNet 全面复兴。',
 },
 'WB-B04': {  # GoogLeNet (2014)
  'solve': '加深加宽网络会让计算量与过拟合风险同步爆炸；问题是在固定计算预算内，如何显著加深网络并提高参数与计算的利用率。',
  'method': '提出 Inception 模块：并行使用 1×1、3×3、5×5 卷积与池化捕获多尺度特征，用 1×1 卷积做降维瓶颈控制计算量；堆叠成 22 层网络，并在中部插入两个辅助分类器缓解梯度消失（推理时丢弃）。',
  'impact': '以约 500 万参数获 ILSVRC 2014 分类冠军（top-5 错误率 6.67%），参数量远小于 VGG；Inception 系列成为高效架构设计范本。多分支结构工程复杂度高，后续被 ResNet 的残差路线在易用性上部分取代。',
  'hook': 'Inception 模块：固定算力内把网络做到 22 层',
 },
}

# ============ P1-b：重复条目改名（详见 logs/*-wkb-batch03.md 与 P1-MERGE-DUPES.md） ============
RENAME = {
 'WB-A50': {  # 原误植 Mamba → MiniMax-01（arXiv 2501.08313）
  'zh': 'MiniMax-01',
  'en': 'MiniMax-01: Scaling Foundation Models with Lightning Attention',
  'venue': 'arXiv 预印本',
  'link': 'https://arxiv.org/abs/2501.08313',
  'authors': 'MiniMax（Aonian Li、Bangwei Gong、Yiran Zhong 等）',
  'tags': ['挑战注意力', '预印本 2025', '模型层', '架构与建模范式'],
  'solve': 'Transformer 注意力对序列长度的二次复杂度，使超长上下文的训练与推理成本高到难以商用；核心问题是线性注意力能否在数千亿参数规模上真正达到顶级模型性能，而不只停留在小尺寸实验。',
  'method': '提出 MiniMax-Text-01：每 8 层中 7 层采用 Lightning Attention（线性注意力）、1 层保留 Softmax 注意力；结合 32 专家 MoE，总参数 456B、每 token 激活 45.9B。配套训练-推理一体化优化与 MoE 通信重叠技术，训练上下文达 100 万 token、推理可外推至 400 万 token；同系列含视觉模型 MiniMax-VL-01。',
  'impact': '论文报告标准基准与 GPT-4o、Claude 3.5 Sonnet 同级，长上下文评测显著领先（4M token 大海捞针 100%），权重开源。它是首批把线性注意力规模化到商用旗舰级的工作之一；超长上下文外推与线性注意力的任务适应性仍需更多独立复现验证。',
 },
 'WB-A52': {  # 原误植 LLaMA → Llama 4（Meta 2025-04 官方发布，无正式论文；rel 中 WB-A33=Llama 3 前身佐证）
  'zh': 'Llama 4',
  'en': 'The Llama 4 herd: Scout, Maverick, and Behemoth（Meta 官方发布说明）',
  'venue': '官方发布说明 · 无正式论文',
  'link': 'https://ai.meta.com/blog/llama-4-multimodal-intelligence/',
  'authors': 'Meta AI（Llama 团队）',
  'tags': ['官方发布说明', '无同行评审'],
  'hook': 'Llama 首次 MoE 化＋原生多模态，上下文号称 10M',
  'solve': '开放权重阵营在 DeepSeek 等冲击下需要新旗舰；核心问题是如何把 Llama 系列升级为原生多模态、稀疏 MoE 与超长上下文，同时维持开放权重策略。',
  'method': '首批发布 Scout（16 专家、总参数 109B、激活 17B、上下文号称 10M token）与 Maverick（128 专家、总参数 400B、激活 17B、上下文 1M），并预览近 2T 参数的 Behemoth 教师模型；采用早期融合的原生多模态预训练与新一代 RL 后训练流程。无正式论文，信息以官方发布说明为准。',
  'impact': '下载量与生态影响力大，但发布后第三方评测与官方口径出现落差，引发基准与“特调版本”争议；其 MoE 化与超长上下文方向仍影响后续开放模型设计。评价该条目应以 LMSYS 等第三方复现数据为准。',
 },
}

for p in papers:
    pid = p['id']
    if pid in CONTENT:
        p.update(CONTENT[pid])
    if pid in RENAME:
        p.update(RENAME[pid])

payload = json.dumps(papers, ensure_ascii=False, separators=(',', ':'))
page.write_text(text[:m.start(2)] + payload + text[m.end(2):], encoding='utf-8')
print('batch03 applied:', len(CONTENT), 'content rewrites +', len(RENAME), 'renames')
