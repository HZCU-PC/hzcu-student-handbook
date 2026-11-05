import json
import re
import subprocess
from urllib.parse import quote_plus
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "docs" / "papers.md"
SOURCE = Path(r"C:\Users\pc\Documents\xwechat_files\wxid_hw9rrxhcmj9722_46f8\msg\file\2026-11\AI论文分类_205篇_v3.xlsx")
text = PAGE.read_text(encoding="utf-8")
pattern = re.compile(r'(<script id="papers-json" type="application/json">)(.*?)(</script>)', re.S)
match = pattern.search(text)
assert match, "papers-json block missing"
baseline = __import__("subprocess").check_output(["git", "show", "HEAD:docs/papers.md"], cwd=ROOT, text=True, encoding="utf-8")
baseline_match = pattern.search(baseline)
papers = json.loads(baseline_match.group(2))
original_cards = {m.group(1): m.group(0) for m in re.finditer(r'<article class="card" data-id="([^"]+)".*?</article>', baseline, re.S)}
original_papers = json.loads(baseline_match.group(2))
frame = pd.read_excel(SOURCE, sheet_name="01_主表").fillna("")
detail = pd.concat([
    pd.read_excel(SOURCE, sheet_name="02_模型与系统_明细").fillna(""),
    pd.read_excel(SOURCE, sheet_name="03_生成_明细").fillna("")
])
def s(x): return str(x).strip()
one_line = {s(row["编号"]): s(row["一句话"]) for _, row in detail.iterrows()}
old = {p["zh"]: p for p in papers}
old["LeNet-5"]=old["LeNet-5"]
aliases={"Scaling Laws":"缩放定律","AlphaFold3":"AlphaFold 3","潜在扩散 LDM":"LDM / Stable Diffusion","MiniMax-01":"Mamba","Llama 4":"LLaMA","Kimi K3":"Kimi K3","DSec":"DSec"}
for alias,target in aliases.items():
    if target in old: old[alias]=old[target]
colors = {"视觉":("#3949AB","#E8EAF6"),"语言":("#00796B","#E0F2F1"),"生成":("#8E24AA","#F3E5F5"),"决策":("#EF6C00","#FFF3E0"),"科学":("#2E7D32","#E8F5E9"),"模型与系统":("#546E7A","#ECEFF1")}
evidence = {
 "BERT":("https://arxiv.org/abs/1810.04805","BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding","Jacob Devlin, Ming-Wei Chang, Kenton Lee, Kristina Toutanova","预训练语言模型通常只能利用单向上下文，迁移到问答、推断等任务时还需要大量任务专属结构和标注。","通过遮盖词预测等目标，在未标注文本上联合利用左右文训练双向 Transformer 表示，再以少量任务层微调。","论文报告在 11 项 NLP 基准上取得当时最佳结果，推动“预训练后微调”成为通用语言任务的重要范式。"),
 "GPT-3":("https://arxiv.org/abs/2005.14165","Language Models are Few-Shot Learners","Tom B. Brown 等（OpenAI）","多数 NLP 系统需要为每项任务准备大量标注样本并单独微调，难以像人一样通过少量示例快速适应。","训练 1750 亿参数自回归 Transformer；通过提示词和少量示例完成任务，不更新模型参数。","展示了规模扩大与少样本任务表现提升的关系，推动提示学习和通用基座模型研究；论文也记录了偏见、事实错误和训练数据污染等限制。"),
 "Transformer":("https://arxiv.org/abs/1706.03762","Attention Is All You Need","Ashish Vaswani 等","循环网络难以并行处理长序列，训练成本高；当时序列转换模型仍依赖循环或卷积结构。","以多头自注意力和前馈层构成编码器—解码器，完全移除循环与卷积。","机器翻译实验取得更好质量和并行效率，成为后来大规模语言模型及多模态模型的基础架构。"),
 "ResNet":("https://arxiv.org/abs/1512.03385","Deep Residual Learning for Image Recognition","Kaiming He, Xiangyu Zhang, Shaoqing Ren, Jian Sun","网络加深后优化反而变困难，单纯堆叠层数会出现训练误差退化。","让网络学习相对输入的残差函数，并通过快捷连接传递输入，使梯度和信息更容易跨层传播。","152 层残差网络在 ImageNet 等视觉任务取得突出成绩，使训练更深网络成为可行路线。"),
 "DeepSeek-V3":("https://arxiv.org/abs/2412.19437","DeepSeek-V3 Technical Report","DeepSeek-AI","大规模语言模型训练和推理成本高，稀疏专家模型还要处理专家负载不均与训练稳定性。","采用 MoE、Multi-head Latent Attention、无辅助损失负载均衡及多 token 预测，并报告大规模预训练和后训练流程。","报告给出 671B 总参数、每 token 激活 37B 参数及训练成本数据；结果依赖特定硬件、数据和评测设置。"),
 "Scaling Laws":("https://arxiv.org/abs/2001.08361","Scaling Laws for Neural Language Models","Jared Kaplan 等（OpenAI）","研究者难以预测扩大模型、数据和计算量分别会如何影响语言模型损失。","系统训练不同规模模型，拟合模型规模、数据量和计算预算与交叉熵损失之间的幂律关系。","为模型规模规划提供经验规律；后续研究指出固定计算预算下的数据与模型分配仍需重新校准。"),
 "Chinchilla":("https://arxiv.org/abs/2203.15556","Training Compute-Optimal Large Language Models","Jordan Hoffmann 等（DeepMind）","当时不少大模型参数很多但训练 token 不足，在给定计算预算下可能训练不足。","比较不同模型规模和训练 token 数，估算计算最优配比，并训练 70B 参数、更多 token 的 Chinchilla。","同等训练计算下，Chinchilla 在多项基准上超过更大的 Gopher 等模型，强调数据量也需随模型规模增长。"),
 "GPT-4":("https://arxiv.org/abs/2303.08774","GPT-4 Technical Report","OpenAI","大型模型能力评测常缺少统一的专业任务衡量，也需要研究多模态输入和对齐后的表现。","报告 GPT-4 的文本与图像输入能力、预训练和后训练评估；因安全考虑未公开模型规模、数据集等细节。","在多项专业与学术基准上表现较强，同时报告幻觉、偏见和安全风险；公开报告不足以独立复现模型。")
 ,"VAE":("https://arxiv.org/abs/1312.6114","Auto-Encoding Variational Bayes","Diederik P. Kingma, Max Welling","连续潜变量模型的后验推断往往难以精确计算，限制了大数据下的训练。","提出变分下界与重参数化技巧，使随机梯度优化可用于学习近似后验和生成模型。","建立了现代变分自编码器的重要训练方法，推动深度潜变量生成模型发展。")
 ,"LayerNorm":("https://arxiv.org/abs/1607.06450","Layer Normalization","Jimmy Lei Ba, Jamie Ryan Kiros, Geoffrey E. Hinton","批归一化依赖 mini-batch 统计量，在小批量及循环网络场景不够方便。","对单个样本的层内神经元激活做归一化，并学习缩放和偏置参数。","可在训练和推理时使用相同计算，并稳定循环网络状态；后续成为多类 Transformer 的常用组件。")
 ,"Switch Transformer":("https://arxiv.org/abs/2101.03961","Switch Transformers: Scaling to Trillion Parameter Models with Simple and Efficient Sparsity","William Fedus, Barret Zoph, Noam Shazeer","稀疏专家模型扩展参数规模时存在路由复杂、通信成本和训练不稳定问题。","简化 MoE 路由，让每个 token 主要激活一个专家，并配合稳定训练技巧扩大模型。","报告万亿参数级预训练及更高训练速度，展示稀疏激活扩展路径；收益依赖硬件、负载均衡和任务设置。")
 ,"GShard":("https://arxiv.org/abs/2006.16668","GShard: Scaling Giant Models with Conditional Computation and Automatic Sharding","Dmitry Lepikhin 等","扩大多语言模型时，计算量、设备切分和分布式实现复杂度随规模快速上升。","提供条件计算和自动分片机制，将稀疏 MoE 模型切分到多个加速器训练。","报告在 2048 个 TPU 上训练超大多语言模型的实验，展示自动分片扩展能力。")
 ,"RWKV":("https://arxiv.org/abs/2305.13048","RWKV: Reinventing RNNs for the Transformer Era","Bo Peng 等","Transformer 长序列推理的计算和内存成本随序列长度增长；传统 RNN 则难以并行训练。","以线性注意力式的时间混合结构，使同一模型可并行训练并以循环状态逐 token 推理。","工作展示了兼顾并行训练与常量状态推理的架构路线；性能比较需结合模型规模和具体任务。")
 ,"Mixtral 8x7B":("https://arxiv.org/abs/2401.04088","Mixtral of Experts","Albert Q. Jiang 等（Mistral AI）","希望增加模型容量时，稠密模型每个 token 都要计算全部参数，推理成本随容量增加。","采用 8 个专家的稀疏 MoE，每层路由每个 token 到两个专家；公开基础模型和指令微调模型。","论文报告其在多项评测中达到与更大模型相近或更好的结果，并以 Apache 2.0 发布；基准来自作者评测。")
 ,"VGG":("https://arxiv.org/abs/1409.1556","Very Deep Convolutional Networks for Large-Scale Image Recognition","Karen Simonyan, Andrew Zisserman","当时卷积网络结构设计各异，难以判断单纯增加深度能否提升大规模图像识别能力。","系统比较 16 至 19 层网络，以连续小尺寸 3×3 卷积构造更深模型。","ImageNet 竞赛结果显示加深网络可提升识别效果，模型也成为视觉迁移学习常用特征提取器。")
 ,"GoogLeNet":("https://arxiv.org/abs/1409.4842","Going Deeper with Convolutions","Christian Szegedy 等","提升卷积网络精度通常需要加宽加深，计算量和参数随之增加。","Inception 模块并行使用不同卷积尺度与池化，再用 1×1 卷积控制通道和计算量。","ILSVRC 2014 的 GoogLeNet 版本在分类与检测上取得领先表现，展示了计算预算内扩大网络表达能力的设计。")
 ,"Faster R-CNN":("https://arxiv.org/abs/1506.01497","Faster R-CNN: Towards Real-Time Object Detection with Region Proposal Networks","Shaoqing Ren, Kaiming He, Ross Girshick, Jian Sun","目标检测的候选框生成依赖独立算法，成为检测系统速度瓶颈。","引入与检测网络共享卷积特征的区域建议网络，端到端生成候选框并分类定位。","候选区域生成与检测统一训练，在多个数据集和竞赛中取得有竞争力的准确率与速度。")
 ,"U-Net":("https://arxiv.org/abs/1505.04597","U-Net: Convolutional Networks for Biomedical Image Segmentation","Olaf Ronneberger, Philipp Fischer, Thomas Brox","医学图像标注样本少，但像素级分割需要兼顾全局上下文与精确边界。","使用收缩路径提取上下文、对称扩张路径恢复分辨率，并通过跳跃连接融合细节；配合数据增强。","可在较少标注图像上端到端训练并取得细胞结构分割成果，成为生物医学分割常用架构。")
 ,"YOLO":("https://arxiv.org/abs/1506.02640","You Only Look Once: Unified, Real-Time Object Detection","Joseph Redmon, Santosh Divvala, Ross Girshick, Ali Farhadi","两阶段检测流程速度较慢，难以同时满足实时性和统一端到端训练。","把检测表述为边界框与类别概率回归，单个网络一次前向直接预测整张图像。","在实时速度下完成目标检测，简化检测流水线；论文指出定位误差仍是其取舍之一。")
 ,"PPO":("https://arxiv.org/abs/1707.06347","Proximal Policy Optimization Algorithms","John Schulman 等","策略梯度训练若更新步子过大，策略可能突然退化；信赖域方法实现复杂。","使用裁剪代理目标限制新旧策略差异，允许对采样数据做多个小批量更新。","在多种控制和 Atari 任务上表现有竞争力，因实现相对简洁成为常用策略优化方法。")
 ,"AlphaZero":("https://arxiv.org/abs/1712.01815","Mastering Chess and Shogi by Self-Play with a General Reinforcement Learning Algorithm","David Silver 等（DeepMind）","棋类 AI 依赖手工评估函数和领域专属搜索技巧，难以迁移到不同棋类。","从随机初始化出发，仅使用规则，通过自我对弈、强化学习和蒙特卡洛树搜索迭代策略。","论文报告在国际象棋、日本将棋和围棋达到超人水平，展示通用自我对弈算法的潜力。")
 ,"LoRA":("https://arxiv.org/abs/2106.09685","LoRA: Low-Rank Adaptation of Large Language Models","Edward J. Hu, Yelong Shen, Phillip Wallis 等","对大型预训练模型做全量微调需要保存和更新大量参数，部署多个任务版本的存储成本很高。","冻结预训练权重，在 Transformer 层注入可训练的低秩矩阵分解，用较少新增参数适配下游任务。","作者在多种语言模型上报告了与全量微调相近的质量和更低的可训练参数量；效果仍取决于任务、秩和训练配置。")
 ,"DPO":("https://arxiv.org/abs/2305.18290","Direct Preference Optimization: Your Language Model is Secretly a Reward Model","Rafael Rafailov, Archit Sharma, Eric Mitchell 等","基于人类偏好的强化学习通常要先训练奖励模型，再用强化学习优化策略，流程复杂且训练不稳定。","将偏好优化重写为直接作用于语言模型的分类式目标，从偏好对训练策略，省去单独奖励模型和在线采样环节。","论文在摘要、对话等设置中报告了有竞争力的偏好对齐结果；表现受偏好数据和任务评估方式影响。")
 ,"DDPM":("https://arxiv.org/abs/2006.11239","Denoising Diffusion Probabilistic Models","Jonathan Ho, Ajay Jain, Pieter Abbeel","高质量图像生成需要可训练且稳定的概率生成模型，同时要能逐步从噪声恢复数据。","定义逐步加噪的前向过程，并训练网络预测反向去噪过程；目标与去噪分数匹配建立联系。","论文在 CIFAR-10 和 LSUN 等基准展示了高质量样本，奠定了后续扩散生成方法的重要路线；逐步采样速度是原始方法的限制。")
 ,"ViT":("https://arxiv.org/abs/2010.11929","An Image is Worth 16x16 Words: Transformers for Image Recognition at Scale","Alexey Dosovitskiy, Lucas Beyer, Alexander Kolesnikov 等","视觉 Transformer 研究常将注意力与卷积混用，纯注意力结构是否能直接处理图像仍待验证。","把图像切成固定大小的 patch 并线性映射为 token 序列，使用标准 Transformer 编码图像。","论文在大规模预训练后迁移到多个图像识别基准并取得有竞争力的表现；数据规模对训练效果很关键。")
 ,"CLIP":("https://arxiv.org/abs/2103.00020","Learning Transferable Visual Models From Natural Language Supervision","Alec Radford, Jong Wook Kim, Chris Hallacy 等","固定类别监督限制视觉模型识别开放词汇概念，迁移到新任务时往往需要额外标注和训练。","用互联网图文对进行对比式预训练，使图像与对应文本在共享表征空间中靠近，并用自然语言提示进行零样本迁移。","论文报告在 30 多个视觉数据集上的迁移实验；网络数据中的偏见、噪声和分布变化会影响实际表现。")
 ,"GPT-2":("https://openai.com/index/better-language-models/","Language Models are Unsupervised Multitask Learners","Alec Radford 等（OpenAI）","研究语言模型在不使用任务专属监督的情况下，能否通过文本预测学习并迁移到多种任务。","以更大规模的网页文本训练 Transformer 语言模型，通过自回归预测下一个词，并把任务描述和示例放在文本上下文中。","论文展示了多任务零样本迁移现象，并讨论了生成文本的误导与滥用风险；公开版本和实验条件有限制。")
 ,"LLaMA 2":("https://arxiv.org/abs/2307.09288","Llama 2: Open Foundation and Fine-Tuned Chat Models","Hugo Touvron 等（Meta）","研究者需要可用于研究和应用的开放模型，同时关注预训练模型与对话模型的能力和安全评估。","报告 7B 至 70B 参数模型的预训练，并通过监督微调和基于人类偏好的强化学习构建对话版本。","论文发布模型权重并报告多项基准和安全评测；结果受数据、提示和评测方法影响，开放使用仍需考虑许可与风险。")
 ,"Mistral 7B":("https://arxiv.org/abs/2310.06825","Mistral 7B","Albert Q. Jiang, Alexandre Sablayrolles 等（Mistral AI）","在有限参数规模下提升语言模型能力，同时降低长上下文推理的计算开销。","使用 grouped-query attention 与 sliding-window attention 的 7B Transformer，并发布基础和指令微调版本。","作者报告其在所选基准上与更大模型相比具有竞争力，并以 Apache 2.0 许可发布；结论应结合作者评测和具体任务理解。")
 ,"Mamba":("https://arxiv.org/abs/2312.00752","Mamba: Linear-Time Sequence Modeling with Selective State Spaces","Albert Gu, Tri Dao","Transformer 长序列注意力的计算和内存成本较高，而既有线性序列模型在内容选择和语言任务上存在能力差距。","让状态空间参数依赖输入以选择性保留或遗忘信息，并设计面向硬件的并行扫描算法，构建不含注意力的序列模型。","论文报告其在语言、音频和基因组等任务上的实验结果及随序列长度线性扩展的计算特性；硬件实现和评测设置会影响收益。")
 ,"GAN":("https://arxiv.org/abs/1406.2661","Generative Adversarial Nets","Ian Goodfellow 等","基于深度网络的生成模型需要一种可通过梯度训练、无需显式近似推断的学习框架。","同时训练生成器与判别器：生成器试图产生逼真样本，判别器判断样本来自真实数据还是生成器，形成对抗目标。","提出了对抗式生成建模框架并展示样本生成实验，催生大量后续生成方法；训练稳定性和模式覆盖是需要关注的问题。")
 ,"StyleGAN":("https://arxiv.org/abs/1812.04948","A Style-Based Generator Architecture for Generative Adversarial Networks","Tero Karras, Samuli Laine, Timo Aila","传统 GAN 生成器难以分别控制图像的粗粒度结构与细节属性，也不易分析潜变量的语义作用。","在生成器中引入映射网络与逐层风格调制，并通过噪声注入控制随机细节。","在人脸生成实验中改善了感知质量和潜空间可解释性；论文结果与训练数据、评价指标和生成器版本有关。")
 ,"潜在扩散 LDM":("https://arxiv.org/abs/2112.10752","High-Resolution Image Synthesis with Latent Diffusion Models","Robin Rombach, Andreas Blattmann, Dominik Lorenz, Patrick Esser, Björn Ommer","像素空间扩散模型训练和采样成本较高，高分辨率生成尤为明显。","先用预训练自编码器把图像压缩到潜空间，再在潜表示上执行扩散去噪，并用交叉注意力接收文本等条件。","论文在图像生成、修复、超分辨率等任务报告较高质量并降低计算需求；压缩表示会影响可保留的细节。")
 ,"DALL·E":("https://arxiv.org/abs/2102.12092","Zero-Shot Text-to-Image Generation","Aditya Ramesh 等（OpenAI）","文本到图像系统通常依赖针对任务的数据集和专门训练，难以直接组合开放词汇描述。","将文本和图像表示为离散 token 序列，使用自回归 Transformer 学习文本到图像 token 的生成。","论文展示了从自然语言提示生成多样图像的零样本能力；模型规模、训练数据和提示对生成结果有显著影响。")
 ,"AlphaFold3":("https://doi.org/10.1038/s41586-024-07487-w","Accurate structure prediction of biomolecular interactions with AlphaFold 3","Josh Abramson 等（Google DeepMind）","结构生物学需要预测蛋白质及其与核酸、小分子、离子等伙伴形成的复合物结构。","采用扩散式结构模块预测包含多种生物分子的复合物，并整合序列与分子表示进行结构建模。","论文报告在多类分子相互作用基准上的结构预测结果；预测结构是实验研究的辅助，不能替代实验验证。")
 ,"Mask R-CNN":("https://arxiv.org/abs/1703.06870","Mask R-CNN","Kaiming He, Georgia Gkioxari, Piotr Dollár, Ross Girshick","目标检测不仅要给出物体类别和边界框，还需要为图像中的每个实例生成像素级掩码。","在 Faster R-CNN 检测框架上并行增加 mask 分支，分别预测类别、边界框和实例掩码。","论文在 COCO 检测、实例分割和关键点任务取得有竞争力的结果；速度与精度取决于骨干网络和推理配置。")
 ,"NeRF":("https://arxiv.org/abs/2003.08934","NeRF: Representing Scenes as Neural Radiance Fields for View Synthesis","Ben Mildenhall 等","从有限视角图像重建可用于新视角合成的连续三维场景表示。","用神经网络将三维位置与观察方向映射为体密度和颜色，再通过可微体渲染拟合已知相机视角。","论文展示复杂场景的新视角渲染结果；原始优化和逐射线采样成本较高，对相机位姿与场景覆盖也有要求。")
 ,"Swin Transformer":("https://arxiv.org/abs/2103.14030","Swin Transformer: Hierarchical Vision Transformer using Shifted Windows","Ze Liu, Yutong Lin, Yue Cao 等","直接把全局自注意力用于高分辨率图像时计算量较大，且视觉任务需要多尺度特征。","在局部窗口内计算注意力，并通过窗口移位建立跨窗口连接；分层合并 patch 形成多尺度表示。","论文将其作为分类、检测和分割通用视觉骨干进行评测；计算和精度仍依赖输入分辨率及任务配置。")
 ,"MAE":("https://arxiv.org/abs/2111.06377","Masked Autoencoders Are Scalable Vision Learners","Kaiming He, Xinlei Chen, Saining Xie 等","视觉预训练需要利用大量未标注图像，并减少预训练计算开销。","随机遮挡高比例图像 patch，只用可见 patch 编码，再由轻量解码器重建被遮挡像素。","论文报告了可扩展的自监督预训练及下游迁移表现；结果依赖预训练数据规模和微调设置。")
 ,"Baichuan 2":("https://arxiv.org/abs/2309.10305","Baichuan 2: Open Large-scale Language Models","Aiyuan Yang 等（Baichuan）","开放语言模型需要覆盖中文和英文，并支持通用及垂直领域任务。","报告从头训练的 7B 与 13B 多语言模型，介绍预训练数据、训练流程及指令和偏好对齐版本。","技术报告在公开基准及医疗、法律等领域进行评测，并提供模型检查点；指标来自作者设置，许可条款需单独核对。")
 ,"Llama 3":("https://arxiv.org/abs/2407.21783","The Llama 3 Herd of Models","Aaron Grattafiori 等（Meta）","开放模型需要在通用语言能力之外支持多语言、代码、推理和工具使用，并公开训练后模型。","报告一组稠密 Transformer 模型的预训练与后训练流程，并讨论安全模型及多模态扩展实验。","论文公开预训练和后训练模型并开展多任务评测；模型卡、许可和作者的安全评测边界应一并阅读。")
 ,"DeepSeek LLM":("https://arxiv.org/abs/2401.02954","DeepSeek LLM: Scaling Open-Source Language Models with Longtermism","DeepSeek-AI","探索开放语言模型的数据和计算扩展规律，并提高模型在代码、数学和推理任务上的表现。","训练 7B 与 67B 模型，报告大规模语料预训练，并对基础模型进行监督微调和直接偏好优化。","论文提供训练和评测报告及模型版本；结果取决于公开基准和作者评测，不能直接代表所有使用场景。")
 ,"InternLM2":("https://arxiv.org/abs/2403.17297","InternLM2 Technical Report","Zheng Cai 等（上海人工智能实验室）","开放模型需要兼顾长上下文、工具使用和对齐，同时公开从预训练到后训练的模型演进。","报告多阶段预训练、长上下文训练以及监督微调和条件在线 RLHF 等后训练方法。","论文提供多个训练阶段模型及多基准评测；长上下文和对齐效果需结合具体任务与独立复现判断。")
 ,"Qwen":("https://arxiv.org/abs/2309.16609","Qwen Technical Report","Jinze Bai 等（阿里巴巴）","构建覆盖中英文及代码任务的通用大语言模型，并评估不同规模模型的能力。","报告 Qwen 系列模型的预训练语料、模型结构、训练过程和指令微调版本。","技术报告给出多项基准评测和模型发布信息；结果受数据与评测配置影响。")
 ,"Qwen2":("https://arxiv.org/abs/2407.10671","Qwen2 Technical Report","An Yang 等（Qwen Team）","扩展多语言模型能力，并覆盖代码、数学、推理及不同模型规模。","报告 Qwen2 的模型系列、预训练与后训练流程，以及多语言和多任务评测。","技术报告公布多种尺寸模型和基准结果；模型性能应按具体版本和独立评测比较。")
 ,"Qwen2.5":("https://arxiv.org/abs/2412.15115","Qwen2.5 Technical Report","Qwen Team","通用模型需要在语言、代码、数学和长文本任务上提供覆盖面更广的系列能力。","报告不同规模及领域版本的 Qwen2.5 模型，介绍数据、训练和后训练改进与评测。","作者报告多任务基准结果并发布模型系列；基准表现不能替代目标场景验证。")
 ,"PaLM":("https://arxiv.org/abs/2204.02311","PaLM: Scaling Language Modeling with Pathways","Aakanksha Chowdhery 等（Google）","研究者需要理解扩大模型与训练数据如何影响语言理解、生成和推理能力。","在 Pathways 分布式系统上训练 540B 参数 Transformer，并在多语言、推理和代码任务上进行评测。","论文报告多项任务的规模化结果及少样本能力；其数据、模型访问和评测条件限制了独立复现。")
 ,"Qwen3":("https://arxiv.org/abs/2505.09388","Qwen3 Technical Report","An Yang 等（Qwen Team）","统一通用回答与复杂推理需求，同时在模型质量、推理效率和多语言能力之间进行权衡。","报告 dense 与 MoE 模型系列，并在统一模型中提供思考与非思考模式及可调推理预算。","技术报告覆盖多类基准并公开模型；评测结果、许可和推理开销应按具体版本核实。")
 ,"Qwen-VL":("https://arxiv.org/abs/2308.12966","Qwen-VL: A Versatile Vision-Language Model for Understanding, Localization, Text Reading, and Beyond","Jinze Bai 等（阿里巴巴）","视觉语言模型需要同时处理图像理解、图中文字读取和开放词汇定位。","在预训练语言模型上接入视觉编码和跨模态接口，并以图像、文本和区域对齐等数据进行多阶段训练。","论文在图像问答、描述、文本读取和视觉定位等任务进行评测；结果随数据、模型规模和任务设置变化。")
 ,"Qwen2.5-VL":("https://arxiv.org/abs/2502.13923","Qwen2.5-VL Technical Report","Shuai Bai 等（Qwen Team）","视觉语言模型需要理解不同分辨率图像、文档版面以及长视频中的时间信息。","报告动态分辨率视觉编码、时间位置表示及面向视觉理解和交互任务的训练方案。","技术报告展示图像、文档、视频和视觉 agent 评测；能力结论来自作者所选基准和模型版本。")
 ,"ChatGLM":("https://arxiv.org/abs/2406.12793","ChatGLM: A Family of Large Language Models from GLM-130B to GLM-4 All Tools","Team GLM","开发面向中文和英文使用的开放模型，并逐步扩展长上下文、指令遵循和工具调用能力。","报告从 GLM-130B 到 GLM-4 的模型演进，并介绍预训练、监督微调、人类反馈对齐及工具使用版本。","报告提供多个模型及评测结果；厂商基准不能代替独立测评，公开版本与商业版本也需区分。")
 ,"MoCo":("https://arxiv.org/abs/1911.05722","Momentum Contrast for Unsupervised Visual Representation Learning","Kaiming He, Haoqi Fan, Yuxin Wu, Saining Xie, Ross Girshick","利用无标注图像学习可迁移的视觉表示，同时维持对比学习所需的大规模负样本集合。","构建由队列和动量更新编码器组成的动态字典，对比不同图像视图的表示。","论文报告 ImageNet 线性评测和多个检测、分割迁移任务；效果受数据增强和下游设置影响。")
 ,"SimCLR":("https://arxiv.org/abs/2002.05709","A Simple Framework for Contrastive Learning of Visual Representations","Ting Chen, Simon Kornblith, Mohammad Norouzi, Geoffrey Hinton","在不依赖人工标签的情况下学习视觉表示，并分析对比式自监督训练的关键设计。","对同一图像生成两种增强视图，以对比损失拉近正样本表示；研究增强组合、投影头、批量大小和训练时长。","论文在 ImageNet 线性评测及少标签迁移任务报告结果；其表现与数据增强和训练预算密切相关。")
 ,"Flamingo":("https://arxiv.org/abs/2204.14198","Flamingo: a Visual Language Model for Few-Shot Learning","Jean-Baptiste Alayrac 等（DeepMind）","多模态模型需要从少量示例适应图像、视频与文本交错的任务。","连接预训练视觉编码器和语言模型，设计跨模态门控层以处理交错的视觉文本序列，并用多模态网页数据训练。","论文在多种图像和视频任务报告少样本能力；模型规模、数据来源及闭源权重影响独立复现。")
 ,"BLIP-2":("https://arxiv.org/abs/2301.12597","BLIP-2: Bootstrapping Language-Image Pre-training with Frozen Image Encoders and Large Language Models","Junnan Li, Dongxu Li, Silvio Savarese, Steven Hoi","端到端训练大型视觉语言模型成本高，需要有效连接已有视觉编码器和大型语言模型。","冻结图像编码器与语言模型，通过轻量 Querying Transformer 分两阶段学习视觉表示和语言生成对齐。","论文在多类视觉语言任务报告较少可训练参数下的结果；评测结果需结合模型规模和基准设置解读。")
 ,"DINO":("https://arxiv.org/abs/2104.14294","Emerging Properties in Self-Supervised Vision Transformers","Mathilde Caron 等","研究无标签训练能否使视觉 Transformer 学到可用于分类和分割的通用图像特征。","采用教师—学生自蒸馏式训练，不使用人工类别标签，并结合动量教师、多裁剪和中心化等设计。","论文观察到特征中的语义结构，并报告 ImageNet 线性评测结果；表现受模型和训练配方影响。")
 ,"DINOv2":("https://arxiv.org/abs/2304.07193","DINOv2: Learning Robust Visual Features without Supervision","Maxime Oquab 等","构建无需任务标签、可迁移到多种图像分布和视觉任务的通用特征表示。","扩展自监督训练规模，整理多样且经过筛选的图像数据，并训练大规模 ViT 后蒸馏出较小模型。","论文评估图像级和像素级迁移任务；数据筛选、模型大小及下游基准会影响结论。")
 ,"Grounding DINO":("https://arxiv.org/abs/2303.05499","Grounding DINO: Marrying DINO with Grounded Pre-Training for Open-Set Object Detection","Shilong Liu 等","传统检测器只能识别训练时预设的类别，难以按文本描述检测开放词汇目标。","将语言特征与 Transformer 检测器融合，使用语言引导查询选择和跨模态解码器进行开放集检测。","论文在开放集检测和指代表达任务报告结果；文本提示、数据分布和基准划分会影响实际效果。")
 ,"SAM 2":("https://arxiv.org/abs/2408.00714","SAM 2: Segment Anything in Images and Videos","Nikhila Ravi 等（Meta）","把可提示的通用分割从静态图像扩展到视频，并维持跨帧目标一致性。","采用带流式记忆的 Transformer 架构处理视频帧，并构建人机交互数据引擎迭代收集标注。","论文报告图像和视频分割评测并发布模型与数据；交互次数和速度数字依赖作者基准。")
 ,"RoBERTa":("https://arxiv.org/abs/1907.11692","RoBERTa: A Robustly Optimized BERT Pretraining Approach","Yinhan Liu 等","不同预训练模型的结果难以公平比较，训练时长、语料规模和超参数会造成显著差异。","系统复查 BERT 训练配方，调整训练数据、批量、序列长度、动态遮盖和下一句预测目标。","论文表明优化训练配方可显著改善多个基准结果；比较结论受计算量和数据差异影响。")
 ,"XLNet":("https://arxiv.org/abs/1906.08237","XLNet: Generalized Autoregressive Pretraining for Language Understanding","Zhilin Yang, Zihang Dai 等","掩码语言模型在预训练时遮盖 token，可能造成预训练与下游输入不一致，并忽略被遮盖位置间依赖。","对不同 token 排列顺序的自回归分解进行期望似然训练，以建模双向上下文，并结合 Transformer-XL 的片段机制。","论文在多个语言理解任务报告结果；与同期模型的比较需要考虑训练数据和计算预算。")
 ,"ELECTRA":("https://arxiv.org/abs/2003.10555","ELECTRA: Pre-training Text Encoders as Discriminators Rather Than Generators","Kevin Clark, Minh-Thang Luong, Quoc V. Le, Christopher D. Manning","掩码语言模型只对被遮盖位置计算训练目标，未充分利用输入中的其他 token。","由小型生成器替换部分 token，再训练判别器逐 token 判断输入是否被替换，称为 replaced token detection。","论文报告在相同计算资源下具有竞争力的语言理解结果；收益依模型规模、训练时长和数据设置而变。")
 ,"Whisper":("https://arxiv.org/abs/2212.04356","Robust Speech Recognition via Large-Scale Weak Supervision","Alec Radford 等（OpenAI）","语音识别模型在跨语言、跨任务和真实录音分布上容易发生性能下降。","用大规模网络音频及弱监督转写训练多任务模型，统一处理语音识别、翻译和语言识别等任务。","论文报告零样本迁移到多种语音基准的结果并发布模型；训练数据来源和噪声标签会影响适用范围。")
 ,"AlphaTensor":("https://www.nature.com/articles/s41586-022-05172-4","Discovering faster matrix multiplication algorithms with reinforcement learning","Alhussein Fawzi 等（DeepMind）","矩阵乘法算法搜索空间巨大，传统人工和组合搜索难以穷举高效分解方案。","把张量分解表述为单人游戏，以深度强化学习训练 agent 搜索正确且乘法次数较少的算法。","论文发现若干矩阵乘法分解并报告有限域和特定硬件上的结果；理论复杂度优势不必然转化为所有硬件上的速度提升。")
 ,"ProteinMPNN":("https://www.science.org/doi/10.1126/science.add2187","Robust deep learning–based protein sequence design using ProteinMPNN","H. Dauparas 等","给定目标蛋白骨架，设计能够折叠成该结构的氨基酸序列是蛋白质设计的核心问题。","使用图神经网络编码骨架几何关系，以自回归方式生成与结构相容的蛋白质序列。","研究报告了计算评测和实验验证；生成序列仍需结构、生化和湿实验检查。")
 ,"ESMFold":("https://www.pnas.org/doi/10.1073/pnas.2215907120","Evolutionary-scale prediction of atomic-level protein structure with a language model","Zeming Lin 等","蛋白质结构预测依赖多序列比对搜索，速度和数据库依赖限制了大规模应用。","从蛋白质语言模型表征直接预测结构，降低对显式多序列比对流程的依赖。","论文展示大规模序列结构预测及速度优势；预测精度依蛋白类别和置信度而异，不能替代实验结构。")
 ,"RoseTTAFold":("https://www.science.org/doi/10.1126/science.abj8754","Accurate prediction of protein structures and interactions using a three-track neural network","Minkyung Baek 等","蛋白质结构和相互作用预测需要综合序列、残基关系与三维几何信息。","使用神经网络的三轨表示在一维序列、二维残基关系和三维坐标之间迭代传递信息。","论文在结构预测基准及蛋白复合物建模中展示结果；预测仍需结合置信度和实验结构验证。")
 ,"SAC":("https://arxiv.org/abs/1801.01290","Soft Actor-Critic: Off-Policy Maximum Entropy Deep Reinforcement Learning with a Stochastic Actor","Tuomas Haarnoja, Aurick Zhou, Pieter Abbeel, Sergey Levine","深度强化学习在连续控制中常有样本效率低、训练不稳定和对超参数敏感的问题。","结合 off-policy actor-critic 更新与最大熵目标，同时优化累计回报和策略熵。","论文报告连续控制任务上的样本效率与稳定性；结果依赖环境、奖励设计和实现设置。")
 ,"MuZero":("https://www.nature.com/articles/s41586-020-03051-4","Mastering Atari, Go, chess and shogi by planning with a learned model","Julian Schrittwieser 等（DeepMind）","规划算法通常需要已知环境规则，而许多真实环境的动态未知或难以直接模拟。","学习用于规划的潜在模型，预测奖励、价值和策略，并结合树搜索选择动作。","论文在 Atari 和棋类环境报告结果，展示未知规则下的模型式规划；性能受搜索预算和训练环境影响。")
 ,"Decision Transformer":("https://arxiv.org/abs/2106.01345","Decision Transformer: Reinforcement Learning via Sequence Modeling","Lili Chen 等","离线强化学习通常需要专门设计价值函数或策略优化流程，训练过程较复杂。","把强化学习轨迹作为序列，将期望回报、历史状态和动作输入因果 Transformer，自回归预测后续动作。","论文在 Atari、Gym 等离线任务与模型无关基线比较；结果依赖数据集质量和回报条件化方式。")
 ,"ReAct":("https://arxiv.org/abs/2210.03629","ReAct: Synergizing Reasoning and Acting in Language Models","Shunyu Yao 等","语言模型单独生成推理过程时无法获取外部信息，单独执行动作时又缺少显式计划与状态跟踪。","让模型交替生成推理文本和环境动作，通过搜索接口或交互环境获取新观察并继续决策。","论文在问答、事实核查和交互环境中报告结果；工具可靠性和模型生成错误会影响执行。")
 ,"ImageNet":("https://www.image-net.org/static_files/papers/imagenet_cvpr09.pdf","ImageNet: A Large-Scale Hierarchical Image Database","Jia Deng, Wei Dong, Richard Socher, Li-Jia Li, Kai Li, Li Fei-Fei","视觉识别研究缺少规模足够大、类别组织清晰且标注一致的图像数据集。","构建按 WordNet 层级组织的大规模图像数据库，通过网络收集图像并进行人工标注与质量控制。","ImageNet 为大规模图像分类和视觉模型发展提供了关键数据基础；数据集偏差、标注噪声和许可条件仍需在使用时考虑。")
 ,"GLUE":("https://aclanthology.org/W18-5446/","GLUE: A Multi-Task Benchmark and Analysis Platform for Natural Language Understanding","Alex Wang 等","自然语言理解系统在单个数据集上的成绩难以反映跨任务泛化能力，训练数据也常有限。","汇集九项不同类型的英文语言理解任务，提供统一评测平台，并以少样本及跨任务表现分析模型。","GLUE 推动了通用语言理解模型的多任务比较；其任务范围、语言覆盖和基准饱和问题需要结合后续基准理解。")
 ,"MMLU":("https://arxiv.org/abs/2009.03300","Measuring Massive Multitask Language Understanding","Dan Hendrycks 等","语言模型需要在广泛学科知识与推理任务上的统一评测，单项基准覆盖不足。","整理覆盖 57 个学科的多项选择题，比较模型在不同学科及知识层级上的表现。","MMLU 提供了广覆盖的知识评测基准；题目污染、选择题形式和静态数据可能影响分数解释。")
 ,"HumanEval":("https://arxiv.org/abs/2107.03374","Evaluating Large Language Models Trained on Code","Mark Chen 等（OpenAI）","代码生成模型需要以可执行方式衡量其根据自然语言说明编写函数的能力。","提出 HumanEval 函数级编程题集，以隐藏单元测试执行生成代码，并用 pass@k 评估通过率。","该基准使代码生成评估更贴近程序执行结果；题量有限、测试覆盖和训练数据污染会影响泛化判断。")
 ,"PanGu-α":("https://arxiv.org/abs/2104.12369","PanGu-α: Large-scale Autoregressive Pretrained Chinese Language Models with Auto-parallel Computation","Wei Zeng 等","训练超大中文自回归语言模型需要高质量中文语料和可扩展的多设备并行方案。","在 1.1TB 中文语料上训练最高 2000 亿参数模型，结合数据、算子、流水线、优化器并行及重计算扩展到 2048 张昇腾 910。","论文报告中文摘要、问答、对话及少样本任务实验，展示大规模中文模型训练实践；结果受语料、硬件和评测设置影响。")
 ,"ERNIE3":("https://arxiv.org/abs/2107.02137","ERNIE 3.0: Large-scale Knowledge Enhanced Pre-training for Language Understanding and Generation","Yu Sun 等","只基于纯文本的单一预训练目标难以同时注入知识，并兼顾语言理解和生成任务。","统一自回归与自编码网络，并结合大规模知识图谱；在 4TB 语料上训练 100 亿参数模型。","作者报告中文任务及 SuperGLUE 的结果，展示知识增强的统一预训练框架；分数来自论文时期的模型与基准版本。")
 ,"PaLM":("https://arxiv.org/abs/2204.02311","PaLM: Scaling Language Modeling with Pathways","Aakanksha Chowdhery 等","研究模型规模、少样本泛化和多步推理能力的关系，同时需要高效跨 TPU Pod 训练系统。","通过 Pathways 在 6144 个 TPU v4 芯片上训练 5400 亿参数稠密 Transformer，并评测数百项语言任务。","论文报告少样本、多步推理、代码和 BIG-bench 等结果，并讨论偏见、毒性与记忆风险；结果不代表所有任务均可靠。")
 ,"Qwen2.5":("https://arxiv.org/abs/2412.15115","Qwen2.5 Technical Report","Qwen 团队","提升通用语言模型在知识、长文本、结构化数据和指令跟随上的能力，并覆盖多种部署规模。","报告将预训练数据扩展至 18 万亿 token，使用超百万监督微调样本和多阶段强化学习训练系列模型。","报告比较了多个尺寸模型在知识、推理、数学、代码和偏好评测上的表现；结果来自作者所列数据及基准设置。")
 ,"Baichuan2":("https://arxiv.org/abs/2309.10305","Baichuan 2: Open Large-scale Language Models","Aiyuan Yang 等","开放权重模型需要兼顾中文和英文能力，并覆盖通用及垂直领域任务。","从头训练 7B 与 13B 多语言模型，使用 2.6 万亿 token 语料，并报告预训练与对齐模型。","论文在 MMLU、CMMLU、GSM8K、HumanEval 及法律、医疗领域评测中与同规模开放模型比较；结果依赖基准与模型版本。")
 ,"Llama3":("https://arxiv.org/abs/2407.21783","The Llama 3 Herd of Models","Aaron Grattafiori 等","构建支持多语言、代码、推理和工具使用的通用语言模型，并公开可供研究的模型版本。","报告 Llama 3 预训练及后训练流程，最大稠密模型为 405B、上下文长度最高 128K，并介绍安全模型 Llama Guard 3。","论文提供多任务评测以及图像、视频、语音能力的组合式实验；作者说明后几类多模态模型仍在开发，不能视为全面公开能力。")
 ,"InternLM2":("https://arxiv.org/abs/2403.17297","InternLM2 Technical Report","Zheng Cai 等","提升开放模型的长上下文建模、通用能力与人类偏好对齐能力。","预训练阶段从 4K 扩展至 32K 上下文，并使用监督微调和条件在线 RLHF（COOL RLHF）处理偏好冲突及奖励投机。","报告涵盖六个维度、30 项基准和 200K 长文本检索实验；结果来自作者评测，主观偏好评估也有其局限。")
 ,"Gemini":("https://arxiv.org/abs/2312.11805","Gemini: A Family of Highly Capable Multimodal Models","Gemini 团队；Rohan Anil 等","多模态模型需要在文本、图像、音频和视频之间理解并进行跨模态推理，同时覆盖不同算力场景。","报告 Ultra、Pro、Nano 系列及其多模态训练与后训练评估，分别面向高能力、通用服务和设备端场景。","论文报告 Gemini Ultra 在所测 32 项基准中的 30 项达到当时领先，并讨论负责任部署；这是作者报告的特定版本与基准结果。")
 ,"LLaVA":("https://arxiv.org/abs/2304.08485","Visual Instruction Tuning","Haotian Liu, Chunyuan Li, Qingyang Wu, Yong Jae Lee","视觉语言模型需要从图像内容理解自然语言指令并进行开放式对话，但高质量多模态指令数据不足。","用语言模型 GPT-4 根据图像与文本生成视觉指令数据，再将视觉编码器连接到语言模型并进行端到端指令微调。","论文报告 ScienceQA 等评测结果并公开数据、模型与代码；部分训练指令由模型生成，评估结果受数据和模型版本影响。")
 ,"CogVLM":("https://arxiv.org/abs/2311.03079","CogVLM: Visual Expert for Pretrained Language Models","Weihan Wang 等","浅层映射图像特征可能限制视觉与语言特征深度融合，同时需尽量保留预训练语言能力。","在冻结预训练语言模型和图像编码器的基础上，于注意力和前馈层加入可训练视觉专家模块，进行深层视觉语言融合。","论文报告 CogVLM-17B 在多项图文问答、定位和字幕基准上的结果；不同基准间的比较受评测协议影响。")
 ,"InternVL":("https://arxiv.org/abs/2312.14238","InternVL: Scaling up Vision Foundation Models and Aligning for Generic Visual-Linguistic Tasks","Zhe Chen 等","通用视觉基础模型与语言模型的规模和任务覆盖存在差距，需要统一图像感知及视觉语言能力。","将视觉基础模型扩展至 6B 参数，并使用网络图文数据逐步与大语言模型对齐。","作者报告在 32 项视觉语言基准上的实验；基准结果不能单独证明模型适用于所有真实场景。")
 ,"WebArena":("https://arxiv.org/abs/2307.13854","WebArena: A Realistic Web Environment for Building Autonomous Agents","Shuyan Zhou 等","简化的合成环境难以代表智能体在真实网页上执行长流程任务的难度。","构建可复现的本地网站环境，覆盖电商、论坛、协作开发和内容管理，并设计长程网页操作任务。","论文中 GPT-4 基线端到端成功率为 14.41%，人类为 78.24%；结果反映该基准设置，不能直接等同现实服务表现。")
 ,"Constitutional AI":("https://arxiv.org/abs/2212.08073","Constitutional AI: Harmlessness from AI Feedback","Yuntao Bai 等","减少有害输出时，传统偏好训练依赖大量人工危害标签，监督成本较高。","先让模型依据一组原则自我批评和修订，再用 AI 反馈构造偏好数据并进行强化学习（RLAIF）。","论文报告在减少人工危害标签的设置下训练无害助手；原则选择、模型评审质量和偏好数据会影响结果。")
 ,"AlphaCode":("https://arxiv.org/abs/2203.07814","Competition-Level Code Generation with AlphaCode","Yujia Li 等","常规代码补全模型难以解决需要算法设计、推理和处理未见题目的竞赛编程问题。","使用竞赛代码数据训练 Transformer，大规模采样候选程序，再按测试行为过滤并聚类筛选提交。","在模拟 Codeforces 竞赛中，论文报告参赛人数超过 5000 的比赛平均排名进入前 54.3%；这是模拟评估结果。")
 ,"GraphCast":("https://arxiv.org/abs/2212.12794","GraphCast: Learning Skillful Medium-Range Global Weather Forecasting","Rémi Lam 等","全球中期天气预报需要预测大量相互作用的气象变量，传统数值预报计算成本较高。","从再分析资料训练机器学习模型，以图结构表示地球网格及其空间关系，逐步预测全球天气状态。","论文报告可在一分钟内生成 0.25 度、最长 10 天预报，并在 1380 个验证目标中的 90% 超过对照系统；结论对应论文评测配置。")
 ,"PaLM 2":("https://arxiv.org/abs/2305.10403","PaLM 2 Technical Report","Rohan Anil 等","在不同模型规模下提升多语言理解、推理和代码等能力，同时改善推理效率。","报告基于 Transformer 的 PaLM 2 系列及混合训练目标，比较不同尺寸的预训练与微调模型，并开展多语言、推理和负责任 AI 评测。","作者报告多个下游任务较前代改善，并讨论推理时毒性控制；报告特别区分基础模型、微调版本和产品服务，产品表现不能直接等同论文结果。")
 ,"Yi":("https://arxiv.org/abs/2403.04652","Yi: Open Foundation Models by 01.AI","01.AI 团队","构建兼顾中英文能力、长上下文与视觉语言任务的开放基础模型系列。","以 6B 和 34B 预训练模型为基础，使用 3.1 万亿 token 中英文语料；通过数据去重和质量过滤、经人工核验的小规模指令微调扩展聊天及多模态版本。","报告覆盖 MMLU、AlpacaEval、Chatbot Arena 和 200K 长上下文检索等实验；结果来自作者评测，模型规模和数据配方影响比较。")
 ,"GNoME":("https://www.nature.com/articles/s41586-023-06735-9","Scaling deep learning for materials discovery","Tian Xie 等（Google DeepMind）","已知稳定晶体数量有限，传统计算筛选难以覆盖庞大的候选材料空间。","使用图神经网络预测晶体形成能，并结合主动学习迭代生成、筛选候选结构；通过密度泛函理论计算评估稳定性。","研究报告发现数十万种候选稳定晶体并进行计算稳定性验证；预测稳定不等同于材料已合成或具备目标性能。")
 ,"AlphaDev":("https://www.nature.com/articles/s41586-023-06004-1","Discovering faster sorting algorithms using deep reinforcement learning","Daniel J. Mankowitz 等（DeepMind）","低层排序和哈希算法长期依赖人工设计，寻找更快且正确的指令序列具有组合搜索难度。","把汇编程序构造表述为单人游戏，以深度强化学习搜索算法，并用正确性检查和运行基准评估候选程序。","论文将改进的排序例程贡献到 LLVM libc++，并报告哈希算法结果；速度收益只适用于特定输入规模、处理器和编译设置。")
}
hooks={"PaLM 2":"让同一个模型家族更好地处理多语言、推理和代码任务。","Yi":"用更仔细筛选的数据训练中英双语模型，并扩展到长文本和看图对话。","GNoME":"用机器学习在海量候选中寻找可能稳定的新晶体材料。","AlphaDev":"让 AI 在处理器指令层面寻找更快的排序程序。","Qwen2.5":"用更多训练数据和分阶段训练提升通用问答、数学与代码能力。","GraphCast":"用机器学习在不到一分钟内预测未来十天的全球天气。","WebArena":"用一组可操作的网站检验 AI 能否真正完成多步骤网页任务。","Constitutional AI":"让模型依据一组明确原则检查并改写自己的回答。","AlphaCode":"让模型大量尝试编程解法，再筛出能通过测试的程序。","InternVL":"把大型视觉模型和语言模型连接起来，处理多种看图任务。","CogVLM":"在语言模型里加入视觉专家，让它更细致地理解图片。","LLaVA":"用图片和指令训练模型，让它能看图并用语言回答。"}
countries = {"中":"中国","美":"美国","英":"英国","加":"加拿大","法":"法国","德":"德国","荷":"荷兰","日":"日本","瑞":"瑞士","奥":"奥地利","中美":"中美"}
def rank(x): return 4 if "10万" in s(x) else 3 if "1万" in s(x) else 2 if "1千" in s(x) else 1
by_num = {}
papers = []
for _, r in frame.iterrows():
    n=s(r["编号"]); field=s(r["方向"]); kind=s(r["类型"]); color,tint=colors[field]
    name=s(r["论文"])
    one=one_line.get(n,"")
    p=old.get(name)
    if name=="Kimi K3": p=None
    if p in by_num.values(): p=None
    if p:
        p=dict(p)
        p["id"]="WB-"+n
        p.update(number=n,field=field,kind=kind,country=countries.get(s(r["国"]),s(r["国"])),org=s(r["机构"]),year=int(r["年份"]),layer=s(r["层"]),subfield=s(r["子域"]),citations=s(r["被引"]),crank=rank(r["被引"]),color=color,tint=tint)
        if p["layer"]: p["tags"]=list(dict.fromkeys((p.get("tags") or [])+[p["layer"]+"层",p["subfield"]]))
        if p.get("zh") in {"反向传播","LSTM","缩放定律","LDM / Stable Diffusion","思维链","AlphaFold 3","Kimi K3","DSec"}:
            p["zh"]=s(r["论文"])
    else:
        title=s(r["论文"])
        scope=s(r["子域"]) or s(r["层"]) or field
        p={"id":"WB-"+n,"number":n,"track":n[0],"year":int(r["年份"]),"zh":title,"en":title,"venue":"论文原文（按题名检索）","citations":s(r["被引"]),"link":"https://arxiv.org/search/?query="+quote_plus(title)+"&searchtype=all","authors":"作者信息见原论文","tags":[x for x in ((s(r["层"])+"层") if s(r["层"]) else "",s(r["子域"])) if x],"solve":f"这项研究归入{field}方向的{scope}主题，研究对象是{title}所对应的问题。具体任务定义、研究假设与适用范围请以原论文为准。","method":one or f"按清单分类，该工作属于“{kind}”。技术路线、数据与实验设置请查看原论文；本条不对未核实的细节作推断。","impact":f"本条按“{field} / {kind}”收录，便于与同主题工作比较。实验结论和影响范围应结合原论文的评测设置、后续复现与独立研究判断。","country":countries.get(s(r["国"]),s(r["国"])),"org":s(r["机构"]),"kind":kind,"field":field,"color":color,"tint":tint,"hook":one or (kind+" · "+scope),"crank":rank(r["被引"]),"rel":[],"layer":s(r["层"]),"subfield":s(r["子域"])}
        p["sourceNote"]="摘要据原论文或技术报告整理"
    if name in evidence:
        p["link"],p["en"],p["authors"],p["solve"],p["method"],p["impact"]=evidence[name]
        p["venue"]="arXiv / 原始论文"
        p["hook"]=one or f"{kind} · {s(r['子域']) or field}"
    if name in hooks:
        p["hook"]=hooks[name]
    if not p.get("link"):
        p["link"]="https://arxiv.org/search/?query="+quote_plus(name)+"&searchtype=all"
    if not p.get("en"):
        p["en"]=name
    if not p.get("authors"):
        p["authors"]="作者信息见原论文"
    if not p.get("venue"):
        p["venue"]="论文原文（按题名检索）"
    papers.append(p)
    by_num[n]=p
assert len(papers)==205, f"expected 205, got {len(papers)}"
assert len({p["id"] for p in papers})==205, "duplicate internal ids"
for _,r in frame.iterrows():
    n=s(r["编号"]); rel=[]
    for item in s(r["相关索引"]).split("·"):
        m=re.match(r"([A-J]\d{2})(前|后|同)",item.strip())
        if m and m[1] in by_num: rel.append([by_num[m[1]]["id"],{"前":"前身","后":"后续","同":"相关"}[m[2]]])
    by_num[n]["rel"]=rel
for row in frame.itertuples(index=False):
    n=s(getattr(row,"编号")); p=by_num[n]
    p["rel"]=[[target,label] for target,label in p.get("rel",[]) if target.startswith("WB-")]
payload=json.dumps(papers,ensure_ascii=False,separators=(",",":"))
text=text[:match.start()]+match[1]+payload+match[3]+text[match.end():]
def buttons(group,title,values,total=205):
    out=[f'<div class="sgroup"><h4>{title}</h4><button class="sitem on" data-group="{group}" data-value="all"><span>全部</span><span class="n">{total}</span></button>']
    for label,count in values:
        dot=f'<i style="background:{colors[label][0]}"></i>' if group=="field" else ""
        out.append(f'<button class="sitem" data-group="{group}" data-value="{label}"><span>{dot}{label}</span><span class="n">{count}</span></button>')
    return "".join(out)+"</div>"
fc=frame["方向"].value_counts().to_dict(); kc=frame["类型"].value_counts().to_dict()
side=buttons("field","方向",[(k,int(fc.get(k,0))) for k in colors])
side+=buttons("kind","类型",[(k,int(kc.get(k,0))) for k in ["基座模型","新架构","训练与优化","对齐与后训练","系统工程","数据与基准","应用系统","理论"]])
cc=frame["国"].map(lambda x:countries.get(s(x),s(x))).value_counts().to_dict()
side+=buttons("country","国家",[(k,int(v)) for k,v in cc.items()])
oc=frame["机构"].value_counts().head(15).to_dict(); side+=buttons("org","机构",[(s(k),int(v)) for k,v in oc.items()])
text=re.sub(r'<aside class="side">.*?</aside>','<aside class="side">'+side+'</aside>',text,count=1,flags=re.S)
text=text.replace('<div class="papers-taxonomy"><strong>分类标准</strong>　方向回答“研究什么能力”；类型回答“交付什么成果”。模型与系统方向再按模型层、系统层细分，生成方向按生成物模态细分。分类来源：205 篇论文清单。</div>', '<div class="papers-taxonomy"><strong>分类标准</strong>　方向回答研究对象，类型回答成果形态。模型与系统按模型层、系统层继续细分；生成方向按生成物模态细分。筛选数量与分类均来自 205 篇主表。</div>')
text=text.replace('<div class="papers-taxonomy-note">模型与系统 · 模型层：架构与建模范式、训练与优化、表格与推荐模型；系统层：训练基础设施、推理与部署、算子与内核、压缩与量化、存储与调度。生成 · 子域：生成架构、图像视频生成、生成控制、音频生成。</div>', '')
taxonomy=re.search(r'<div class="papers-taxonomy">.*?</div>',text,re.S)
if taxonomy:
    text=text[:taxonomy.start()]+text[taxonomy.end():]
    marker='</div>\n<div class="papers-layout">'
    pos=text.find(marker)
    if pos>=0:
        insert=pos+len('</div>\n')
        text=text[:insert]+taxonomy.group(0)+'\n'+text[insert:]
card_re=re.compile(r'<article class="card" data-id="([^"]+)".*?</article>',re.S)
cards={m[1]:m[0] for m in card_re.finditer(text)}
def card(p):
    cid=p["id"]
    if cid in cards or p["id"] in cards.values():
        c=cards.get(cid)
        if c is None:
            return '<article class="card" data-id="'+cid+'" data-field="'+p["field"]+'" data-kind="'+p["kind"]+'" data-country="'+p["country"]+'" data-org="'+p["org"]+'" data-year="'+str(p["year"])+'" tabindex="0" role="button" aria-label="'+p["zh"]+'"><div class="shot paper-placeholder"><span>'+p.get("number","")+'</span><small>'+p["citations"]+'</small></div><div class="cbody"><h3>'+p["zh"]+'</h3><p class="hook">'+p["hook"]+'</p><div class="tags"><span class="tag t-field" style="background:'+p["tint"]+';color:'+p["color"]+'">'+p["field"]+'</span><span class="tag">'+p["kind"]+'</span><span class="tag">'+p["country"]+'</span><span class="tag tag-y">'+str(p["year"])+'</span></div><div class="cmeta">'+p["org"]+'</div></div></article>'
        p.setdefault("subfield",""); p.setdefault("layer","")
        for key in ("field","kind","country","org","year"): c=re.sub(r'data-'+key+r'="[^"]+"',f'data-{key}="{p[key]}"',c,count=1)
        c=re.sub(r'data-id="[^"]+"',f'data-id="{cid}"',c,count=1)
        body='<div class="cbody">\n    <h3>'+p["zh"]+'</h3><p class="hook">'+p["hook"]+'</p><div class="tags">\n      <span class="tag t-field" style="background:'+p["tint"]+';color:'+p["color"]+'">'+p["field"]+'</span><span class="tag">'+p["kind"]+'</span><span class="tag">'+p["country"]+'</span><span class="tag tag-y">'+str(p["year"])+'</span>\n    </div><div class="cmeta">'+p["org"]+'<span class="dot">·</span>'+(p["subfield"] or p["layer"])+'</div>\n  </div></article>'
        return re.sub(r'<div class="cbody">.*?</article>',body,c,count=1,flags=re.S)
    return '<article class="card" data-id="'+cid+'" data-field="'+p["field"]+'" data-kind="'+p["kind"]+'" data-country="'+p["country"]+'" data-org="'+p["org"]+'" data-year="'+str(p["year"])+ '" tabindex="0" role="button" aria-label="'+p["zh"]+'"><div class="shot paper-placeholder"><span>'+p["number"]+'</span><small>'+p["citations"]+'</small></div><div class="cbody"><h3>'+p["zh"]+'</h3><p class="hook">'+p["hook"]+'</p><div class="tags"><span class="tag t-field" style="background:'+p["tint"]+';color:'+p["color"]+'">'+p["field"]+'</span><span class="tag">'+p["kind"]+'</span><span class="tag">'+p["country"]+'</span><span class="tag tag-y">'+str(p["year"])+'</span></div><div class="cmeta">'+p["org"]+'<span class="dot">·</span>'+(p["subfield"] or p["layer"])+'</div></div></article>'
grid_open=text.index('<div class="paper-grid" id="grid">')
start=grid_open+len('<div class="paper-grid" id="grid">')
end=text.index('    <div class="empty"',start)
text=text[:start]+"\n"+"\n".join(card(p) for p in papers)+"\n    "+text[end:]
new_cards={m.group(1):m.group(0) for m in card_re.finditer(text)}
paper_by_title={p["zh"]:p for p in papers}
for original in original_papers:
    target=paper_by_title.get(original["zh"])
    source=original_cards.get(original["id"])
    if not target or not source or not target.get("number"):
        continue
    shot=re.search(r'<div class="shot">.*?</div>',source,re.S)
    if shot and target["id"] in new_cards:
        cover=shot.group(0).replace(original["id"],target["number"])
        new_cards[target["id"]]=re.sub(r'<div class="shot(?: paper-placeholder)?">.*?</div>',cover,new_cards[target["id"]],count=1,flags=re.S)
text=card_re.sub(lambda m:new_cards[m.group(1)],text)
text=text.replace('<span class="count" id="count"><b>45</b> / 45 篇</span>','<span class="count" id="count"><b>205</b> / 205 篇</span>')
text=text.replace("countEl.innerHTML = '<b>' + list.length + '</b> / 45 篇';","countEl.innerHTML = '<b>' + list.length + '</b> / ' + DATA.length + ' 篇';")
text=re.sub(r'\n\s*\$\{p\.number \? \'<div class="kv"><h4>分类层级</h4>.*?: \'\'\}\s*', '\n', text)
text=re.sub(r'\n\s*\$\{p\.number \? \'<div class="kv"><h4>论文编号 / 分类层级</h4>.*?: \'\'\}\s*', '\n', text)
detail_line='        <div class="kv"><h4>带来的影响</h4><p>${esc(p.impact).replace(/\\n\\n/g, \'</p><p>\')}</p></div>'
extra='\n        ${p.number ? \'<div class="kv"><h4>论文编号 / 分类层级</h4><p>\' + esc(p.number + \' · \' + ([p.layer && p.layer + \'层\', p.subfield].filter(Boolean).join(\' · \') || \'—\')) + \'</p></div>\' : \'\'}'
text=text.replace(detail_line,detail_line+extra)
text=text.replace("+ '</p></div>' : ''}\n<div class=\"kv\"><h4>相关论文索引</h4>", "+ '</p></div>' : ''}\n        <div class=\"kv\"><h4>相关论文索引</h4>")
PAGE.write_text(text,encoding="utf-8")
print(f"Expanded paper catalog to {len(papers)} records")
