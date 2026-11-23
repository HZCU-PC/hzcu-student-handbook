"""CUR batch05: JSON patch only. Merged after user 继续扩写. See P1-VOICE.md."""
import json
import re
from pathlib import Path

PAGE = Path(__file__).resolve().parents[1] / "docs" / "papers.md"
PAT = re.compile(r'(<script id="papers-json" type="application/json">)(.*?)(</script>)', re.S)
TPL = "核心问题，是如何"

CONTENT = {
    "WB-A37": {
        "hook": "Qwen 系的中期迭代：更长的上下文与更重的代码/数学",
        "solve": "Qwen2 已经证明全尺寸开放模型可以打，但社区真正用的是 2.5 这一代：更长上下文、更强的代码与数学，以及更清晰的许可边界。",
        "method": "在 Qwen2 架构上继续放大预训练与后训练数据，强调长文本、工具与代码混合；发布多个尺寸并保持部分权重 Apache 2.0。具体数据配方以官方技术报告为准。",
        "impact": "Qwen2.5 成为 2024–2025 国内部署与二次微调最常见的基座之一。榜单分数会随评测版本变化，选型仍要看任务与许可。",
    },
    "WB-A42": {
        "hook": "智谱把 GLM 推到多模态与 Agent 同一代",
        "solve": "ChatGLM 之后，市场要的不只是双语聊天，而是能看图像、调工具、跟进的 GLM-4 级助手。",
        "method": "延续 GLM 架构路线，扩展多模态输入与工具调用；对齐阶段覆盖 SFT 与偏好学习。公开材料以智谱发布说明为主，细节少于部分国际技术报告。",
        "impact": "GLM-4 在国内 API 与开源权重生态里占重要位置。多模态与 Agent 能力依赖具体产品版本，不宜用单次评测代表全部场景。",
    },
    "WB-A43": {
        "hook": "零一万物 Yi 系列的开放权重冲刺",
        "solve": "2024 年开放模型竞争白热化，Yi 要在中英双语与长上下文上给出有辨识度的基座，同时保持可商用许可。",
        "method": "大参数量预训练加长上下文扩展；后续迭代到 Yi-1.5 等版本改进数学与代码。训练数据与配比见官方披露，外部难以完全复现。",
        "impact": "Yi 在中文开放社区有稳定用户群。版本迭代快，旧 checkpoint 与新版能力不可混谈。",
    },
    "WB-A46": {
        "hook": "运营商背景的大模型 TeleChat",
        "solve": "电信场景需要可控、可私有化部署的对话模型，而不是只能调用公有 API。TeleChat 面向这类需求发布系列权重。",
        "method": "中英预训练加行业语料微调，提供多个参数规模。论文与报告相对简洁，工程部署文档重于学术细节。",
        "impact": "在政务、运营商私有化项目里常见。通用 benchmark 上未必是最高分，优势在合规与落地配套。",
    },
    "WB-A49": {
        "hook": "Kimi 系开放权重 K2 与长文本路线",
        "solve": "月之暗面以长上下文产品出名，K2 把同一路线延伸到开放权重，供社区本地部署与微调。",
        "method": "大规模预训练配合长文本训练与推理优化；具体架构与数据以官方发布为准。K2 与网页版 Kimi 产品并非同一交付形态。",
        "impact": "长文档、检索增强类应用开发者关注度高。开放权重的能力边界需以官方评测与自行测为准。",
    },
    "WB-B16": {
        "hook": "不用人工标签也能学视觉表征",
        "solve": "ImageNet 标注贵，自监督能否只从图像本身学出可用的特征？DINO 用 student-teacher 和 momentum encoder 在 ViT 上试这条线。",
        "method": "两路网络：teacher 参数是 student 的慢速指数滑动平均；student 只看局部 crop，teacher 看更大视图，用交叉视角一致性当训练信号，无需类别标签。",
        "impact": "k-NN 探针和下游微调都显示特征质量不错，影响后续 MAE、DINOv2 等自监督视觉路线。仍依赖增强与架构选择，不是「完全无归纳偏置」。",
    },
    "WB-B22": {
        "hook": "把 CLIP 和 LLM 接起来聊图",
        "solve": "CLIP 懂图文对齐，LLM 懂对话，但两者分开。LLaVA 问：能否用简单投影层把视觉特征接进语言模型，用对话数据教它「看图说话」？",
        "method": "冻结 CLIP 视觉编码器，训练线性层映射到 LLM 词嵌入空间；先用图文对齐的 instruction 数据做 stage-1，再用 GPT 生成的多轮对话做 stage-2。",
        "impact": "引爆开源多模态对话模型浪潮（LLaVA-1.5 等）。幻觉、细粒度计数错误仍是通病，接什么 LLM 决定能力上限。",
    },
    "WB-B23": {
        "hook": "Qwen 视觉语言一体化",
        "solve": "通用 LLM 已有 Qwen，视觉任务需要同一技术栈上的 VLM，而不是另起炉灶。",
        "method": "视觉塔 + 跨模态 connector + Qwen 语言 backbone；多阶段训练覆盖对齐、指令微调。后续 Qwen2-VL / 2.5-VL 继续迭代分辨率与视频。",
        "impact": "国内 VLM 部署与评测里出现频率极高。不同版本支持的分辨率、视频长度差异大，部署前要对表文档。",
    },
    "WB-C01": {
        "hook": "词向量：上下文里经常一起出现的词，向量也靠近",
        "solve": "one-hot 词表太大，词与词之间没有「相似度」。word2vec 用大规模语料，让向量空间里的距离反映用法。",
        "method": "Skip-gram / CBOW：预测上下文或从上下文预测中心词；负采样降低训练成本。得到静态词向量，一词一向量，不含多义。",
        "impact": "2010 年代 NLP 默认第一步。后来被 ELMo、BERT 等上下文向量取代，但「分布式表示」思想仍在。",
    },
    "WB-C06": {
        "hook": "「Text-to-Text」：什么都转成文本序列",
        "solve": "NLP 任务格式五花八门，T5 干脆统一成：输入文本 → 输出文本，翻译、摘要、分类都写成生成问题。",
        "method": "Encoder-decoder Transformer；预训练用 span corruption（随机挖空再预测）；规模从 base 到 11B，下游任务只改 prompt 字符串。",
        "impact": "Google 系预训练范式的重要一支，影响 UL2、Flan-T5。纯生成式统一也有任务不适配的时候，分类有时不如 encoder-only 省事。",
    },
    "WB-D08": {
        "hook": "「Let's think step by step」从哪来",
        "solve": "大模型算应用题常一步错全盘错。Chain-of-Thought 发现：在提示里要求写出中间步骤，往往能把多步推理拉对。",
        "method": "Few-shot 示例里包含推理链；模型生成答案前先输出中间文字。也有 zero-shot 触发句。不是改权重，是改输入格式。",
        "impact": "成为提示工程基本功，也催生 CoT 微调、自我一致性等后续工作。链可以是瞎编的，看起来对但逻辑跳步仍会发生。",
    },
    "WB-E01": {
        "hook": "生成器和判别器互相较劲",
        "solve": "生成清晰图像很难。Goodfellow 等人让两个网络对赌：一个造假，一个鉴别，看谁先骗过谁。",
        "method": "生成器 G 把噪声映射成样本；判别器 D 区分真图与 G 的输出。min-max 博弈训练，理论上收敛到数据分布（实践中常 Mode collapse、训练不稳）。",
        "impact": "开启深度学习生成图像时代，影响后续 StyleGAN、扩散模型。现在图像生成主流是扩散，GAN 仍在一些实时场景使用。",
    },
    "WB-E03": {
        "hook": "从噪声一步步 denoise 出图",
        "solve": "生成模型除了 GAN，能否定义一个稳定的目标？DDPM 把生成看成学习逆转一个固定的加噪过程。",
        "method": "前向过程逐步加高斯噪声；网络学习预测每一步的噪声或 x0。采样时从纯噪声迭代去噪。训练目标相对 GAN 更稳定但采样慢。",
        "impact": "扩散模型复兴的数学底座，连接 Score matching 与 LDM、Stable Diffusion。采样步数与质量/速度的权衡仍是工程重点。",
    },
    "WB-H04": {
        "hook": "先检索，再生成——RAG 这个名字",
        "solve": "LLM 参数里塞不下的知识、会过期的知识，靠增大模型也解决不了。RAG：外挂检索，把查到的段落塞进 prompt 再答。",
        "method": "索引文档 → 查询编码 → 取 top-k 段落 → 与问题拼成上下文 → LLM 生成答案。检索质量、分块、重排序都影响最终效果。",
        "impact": "企业知识库问答的默认架构。检索错则生成再流畅也是胡编；和 GraphRAG、Self-RAG 等变体一起构成 2024–2025 检索增强主线。",
    },
    "WB-I01": {
        "hook": "ImageNet：深度学习比赛的燃料",
        "solve": "以前视觉数据集小、类别少，算法改进难比较。ImageNet 提供百万级标注图像和 ILSVRC 竞赛，让「更大数据 + 更深网络」可验证。",
        "method": "WordNet 层次组织类别；众包标注；每年竞赛固定 train/val 划分。2012 AlexNet 在此夺冠成为转折点。",
        "impact": "几乎定义了 2010 年代视觉研究节奏。数据有偏见、类别偏物体中心；现在更大规模预训练常用 web 数据，但 ImageNet 仍是基线。",
    },
    "WB-G06": {
        "hook": "KV cache 像酒店分页订房",
        "solve": "LLM 推理时 KV cache 占显存，batch 一大就 OOM。vLLM 用 PagedAttention 把 cache 切成块、像虚拟内存一样分配。",
        "method": "物理 KV 块不连续存放，按序列逻辑映射；Continuous batching 动态插入新请求。开源 serving 框架 vLLM 实现这一套。",
        "impact": "高并发 API serving 的事实标准之一，影响 TGI、SGLang 等后续系统。吞吐提升依赖硬件与模型结构，不是万能倍数。",
    },
    "WB-B17": {
        "hook": "读几幅图就能模仿的 Flamingo",
        "solve": "少样本视觉问答：给模型看几个图文示例，它应能回答新图的问题。Flamingo 把 frozen LM 和视觉特征用 gated cross-attention 接起来。",
        "method": "Perceiver Resampler 压缩视觉 token；插入 LM 层的 cross-attention 只看图像；大规模网页图文预训练。",
        "impact": "少样本 VLM 里程碑，思路影响 BLIP-2、LLaVA 等。冻结 LM 省训练成本，但上限受底座 LM 与对齐数据约束。",
    },
    "WB-F01": {
        "hook": "氨基酸序列 → 三维结构",
        "solve": "实验测蛋白结构慢且贵。AlphaFold2 在 CASP14 上把预测精度推到接近实验，震惊结构生物学界。",
        "method": "MSA 与 pair representation；Evoformer 迭代更新；结构模块输出原子坐标。用 PDB 与自蒸馏数据训练。",
        "impact": "AlphaFold DB 放出大量预测结构，加速下游研究。预测不等于功能机制；复合物、动态构象仍需要专门方法（见 AlphaFold3 等）。",
    },
}


def main() -> None:
    text = PAGE.read_text(encoding="utf-8")
    m = PAT.search(text)
    if not m:
        raise SystemExit("papers-json missing")
    papers = json.loads(m.group(2))
    by_id = {p["id"]: p for p in papers}
    bad = [i for i in CONTENT if i not in by_id]
    if bad:
        raise SystemExit(f"unknown ids: {bad}")
    skip = [i for i in CONTENT if TPL not in by_id[i].get("solve", "")]
    if skip:
        raise SystemExit(f"not template (refusing): {skip}")
    for pid, fields in CONTENT.items():
        by_id[pid].update(fields)
    payload = json.dumps(papers, ensure_ascii=False, separators=(",", ":"))
    PAGE.write_text(text[: m.start(2)] + payload + text[m.end(2) :], encoding="utf-8")
    print("batch05 CUR applied:", len(CONTENT))


if __name__ == "__main__":
    main()
