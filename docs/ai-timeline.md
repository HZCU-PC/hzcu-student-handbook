# AI 发展时间线

本专题用几个关键节点串起人工智能，尤其是神经网络与深度学习的发展。它是帮助读者理解论文背景的**教学导览**，不是人工智能全部历史的完整年表，也不代表学界唯一的分期方式。节点按“提出了什么问题或方法、后来有什么可核查影响”选取；每项都附论文原文或学术机构资料，方便继续查证。

> **阅读提示：**从上到下按时间浏览。每个时期先交代背景，再列代表节点；“历史意义”说明它与本专题的关系。年份按论文正式发表或机构记载的事件年份标注，预印本与产品发布会特别注明。

<div class="ai-timeline" markdown>

## 早期思想与神经网络萌芽 · 1943—1985

人工智能并非从深度学习开始。早期研究一方面尝试用逻辑和符号表示知识，另一方面也探索神经元式计算模型。这个时期的节点说明神经网络思想的早期来源；它们不是今天深度学习的直接等同物。

<div class="ai-timeline__events" markdown>

### 1943 · 神经网络的数学模型

Warren McCulloch 与 Walter Pitts 发表神经活动逻辑模型，尝试回答一个基础问题：由许多简单神经元组成的网络，能否完成逻辑推理？他们把神经元简化成接收信号后“触发/不触发”的单元，再用网络连接表示逻辑关系。这是理论模型，并不是一台能像人一样思考的机器，也没有现代神经网络的训练方法。

**历史意义：**为后续人工神经网络研究提供了重要的数学化模型。这里说的是“早期起点”，不意味着现代神经网络已在 1943 年成形。

[来源：Computer History Museum 时间线](https://www.computerhistory.org/timeline/ai-robotics/)

### 1950 · 图灵与“机器能否思考”

Alan Turing 在哲学期刊 *Mind* 发表《计算机器与智能》，讨论“机器能思考吗”这个问题为什么难以直接定义。他提出用“模仿游戏”来把讨论变得更具体：如果评判者只通过文字交流，无法可靠地区分对话对象是人还是机器，我们可以据此讨论机器表现出的智能。后来人们常把这种思路简称为“图灵测试”，但论文原文的讨论比一个简单的及格测试更丰富；它也不是今天公认的、衡量所有人工智能能力的统一标准。

**历史意义：**这篇论文把人工智能的一项核心问题带入可公开讨论的研究框架，也提醒读者区分“看起来像人类的对话表现”和更广泛的智能问题。

[来源：*Mind* 原始论文（Oxford Academic）](https://doi.org/10.1093/mind/LIX.236.433)

### 1956 · 达特茅斯研讨会与“人工智能”名称

John McCarthy、Marvin Minsky、Nathaniel Rochester 与 Claude Shannon 为一次夏季研讨会撰写提案，提出集中讨论如何让机器模拟学习和智能行为。Computer History Museum 将这次 1956 年的研讨会视为人工智能领域的创建事件之一，并记载“人工智能”这一名称与研讨会提案相关。参加者研究的路线很多，包括逻辑推理、语言和神经网络，因此它不是一场只讨论神经网络的会议。

**历史意义：**这是理解 AI 作为一个研究领域如何形成的重要背景，也能帮助读者看到神经网络只是人工智能历史中的一条路线。

[来源：Computer History Museum，Chatbots Decoded](https://computerhistory.org/stories/chatbots-decoded/) · [Computer History Museum，AI 时间线](https://www.computerhistory.org/timeline/ai-robotics/)

### 1958 · 感知机

Frank Rosenblatt 展示感知机及其电子实现。可以把它理解为一个简单的分类器：它接收一组输入特征，给每个特征分配权重，再根据加权结果把样本分到不同类别。学习过程会根据例子调整这些权重。早期演示让“机器从样例中学习”成为可实验的研究方向；不过，单层感知机不能解决所有分类问题，网络结构和能力都有边界。

**历史意义：**它把可训练的神经网络模型带入实验和工程实践，也为后来关于单层模型能力的讨论提供了背景。

[来源：Computer History Museum，Chatbots Decoded](https://computerhistory.org/stories/chatbots-decoded/)

### 1969 · 感知机的能力边界

Marvin Minsky 与 Seymour Papert 出版《感知机》，从数学上分析当时单层感知机能处理哪些模式、哪些模式难以处理。例如，单层感知机无法直接表示 XOR（异或）这类需要非线性分界的简单逻辑关系。书中讨论的是特定结构的能力限制，不能简单概括成“神经网络都不行”，也不应把它单独当作后来神经网络研究减缓的唯一原因。

**历史意义：**它记录了研究者对早期模型局限的严肃分析，帮助解释为什么多层网络及其训练方法后来成为重要问题，也避免把复杂的研究史简化为“某本书终结了神经网络”。

[来源：MIT Press，*Perceptrons*](https://mitpress.mit.edu/9780262130431/perceptrons/)

### 1982 · Hopfield 网络

John Hopfield 提出一种能够储存模式、并在输入受干扰时恢复相似模式的网络。直观地说，网络像一个有许多可能状态的系统：输入残缺或带噪声时，连接关系会使状态逐步趋向某个已储存的稳定模式。Hopfield 借助统计物理学方法分析这些状态。诺贝尔奖官方资料把这项工作列为神经网络机器学习发展的基础贡献之一。

**历史意义：**它显示 1980 年代的神经网络研究并未中断，并为后续能量模型等研究提供重要背景。

[来源：诺贝尔奖官方介绍](https://www.nobelprize.org/laureate/1037)

### 1985 · Boltzmann 机

Geoffrey Hinton、Terrence Sejnowski 与 David Ackley 研究 Boltzmann 机，一种带有隐含单元和随机状态的神经网络。模型通过例子调整连接，使网络更容易产生训练数据中常见的模式；隐含单元可以表示数据中不直接标注出来的特征。它把统计物理的概率与能量概念用于机器学习，也为后来深度网络的预训练方法提供了思路。

**历史意义：**这一成果连接了 Hopfield 网络、Hinton 后续的深度学习研究与现代神经网络发展脉络，补上早期神经网络研究在 1982 到 1986 年间的重要进展。

[来源：诺贝尔奖官方背景资料](https://www.nobelprize.org/prizes/physics/2024/popular-information/)

</div>

## 反向传播与深度学习条件成熟 · 1986—2011

1980 年代中期，反向传播的研究推动了多层神经网络训练。此后相关方法持续发展，但数据规模、计算能力和训练技术等条件限制了更大规模模型的应用。与其称作“神经网络被全体学界否定的30年”，不如具体描述当时方法的能力边界和研究环境；不同研究方向并非同步停滞。

<div class="ai-timeline__events" markdown>

### 1986 · 反向传播与多层网络训练

David Rumelhart、Geoffrey Hinton 与 Ronald Williams 在 *Nature* 发表反向传播研究。训练网络时，先比较模型输出与正确答案之间的差距，再把误差信息从输出层逐层传回前面的层，据此调整连接权重。重复这个过程后，模型有机会学会把输入转换成适合完成任务的内部表示。这里的“隐藏单元”就是输入和最终答案之间、由模型自行形成中间计算的部分。

**历史意义：**这是多层神经网络训练史上的重要论文，也为理解后来深度学习如何训练提供关键背景。反向传播的数学思想更早已有研究，因此不应写成该论文“发明了反向传播”。

[来源：Nature 原文](https://doi.org/10.1038/323533a0) · [诺贝尔奖背景资料](https://www.nobelprize.org/prizes/physics/2024/popular-information/)

[论文库介绍：B01 · 反向传播](paperweb/paper.html?id=B01)

### 1998 · LeNet 与手写文字识别

Yann LeCun、Léon Bottou、Yoshua Bengio 与 Patrick Haffner 总结了卷积网络在手写数字和文件识别中的应用。LeNet 这类网络通过局部卷积和逐步汇集图像信息，从像素中学习识别文字所需的特征；相比人工为每种笔画规则编程，系统可以从标注样本中学习。论文展示了从输入图像到识别结果的整体系统，也讨论了它在真实文件处理中的工程环节。

**历史意义：**它说明卷积神经网络在 AlexNet 之前已用于实际识别任务，是连接早期神经网络与 2012 年视觉竞赛突破的重要桥梁。

[来源：IEEE，*Gradient-Based Learning Applied to Document Recognition*](https://doi.org/10.1109/5.726791)

[论文库介绍：B02 · LeNet-5](paperweb/paper.html?id=B02)

### 2006 · 深层自编码器与逐层预训练

Geoffrey Hinton 与 Ruslan Salakhutdinov 发表深层自编码器研究。自编码器先把输入压缩成较短的内部表示，再尝试从这个表示重建原始输入；论文提出先逐层初始化网络权重，再整体微调，使较深的网络更容易学到有用的压缩表示。作者在高维数据降维实验中展示了这一做法的效果。

**历史意义：**这项工作是 2000 年代深层神经网络重新受到关注的重要节点之一，但深度学习的复兴还依赖数据、硬件和其他研究进展，不能归因于单篇论文。

[来源：*Science* 原文（PubMed 书目与摘要）](https://doi.org/10.1126/science.1127647)

### 2010—2011 · ImageNet 大规模视觉评测

ImageNet 大规模视觉识别挑战赛（ILSVRC）提供大量带有类别标签的图像，以及共同的训练、验证和测试规则。研究团队可以用同一任务提交结果，比较模型识别图像的准确程度。这样的数据和评测基础设施让改进是否有效更容易被检验。它不是单篇论文，也不是某一种模型，而是推动视觉研究可比较、可复现的重要条件。

**历史意义：**要理解 2012 年 AlexNet 的结果，必须同时看到大型标注数据集、GPU 计算和竞赛评测这些条件。

[来源：AlexNet 论文对 ILSVRC 的说明（NeurIPS）](https://proceedings.neurips.cc/paper/2012/hash/c399862d3b9d6b76c8436e924a68c45b-Abstract.html) · [Computer History Museum](https://computerhistory.org/stories/chatbots-decoded/)

</div>

## 深度学习在视觉与博弈任务中取得突破 · 2012—2016

这一阶段的代表性进展集中在深层网络、数据集和 GPU 计算的结合上。以下节点记录的是具体论文和竞赛结果；“转折”是基于这些结果及机构历史资料作出的概括，不代表单一论文独自造成整个领域变化。

<div class="ai-timeline__events" markdown>

### 2012 · AlexNet 与 ImageNet

Alex Krizhevsky、Ilya Sutskever 与 Geoffrey Hinton 的卷积神经网络在 ILSVRC 2012 获胜。卷积网络会逐层从图像中提取由简单到复杂的视觉特征；论文报告模型在测试集 top-5 错误率为 15.3%，第二名为 26.2%（top-5 指正确类别是否出现在模型给出的前五个预测中）。研究还使用 GPU 加速计算，并通过 dropout 减少训练时对特定神经元的过度依赖。这个结果来自模型、数据和计算资源的结合。

**历史意义：**这是有明确竞赛数据支撑的代表节点。Computer History Museum 将其描述为推动深度学习进入新阶段的重要事件之一；我们据此称其为“重要转折”，而不写成“AI 革命由 AlexNet 单独开启”。

[来源：NeurIPS 论文](https://proceedings.neurips.cc/paper/2012/hash/c399862d3b9d6b76c8436e924a68c45b-Abstract.html) · [Computer History Museum](https://computerhistory.org/stories/chatbots-decoded/)

[论文库介绍：B03 · AlexNet](paperweb/paper.html?id=B03)

### 2014 · 生成对抗网络（GAN）

Ian Goodfellow 等人提出生成对抗网络（GAN），用两个相互竞争的网络学习生成数据。生成器负责造出看起来像训练样本的内容，判别器尝试分辨真实样本与生成样本；生成器根据判别结果改进，判别器也持续变强。这个过程类似“造假者”和“鉴别者”彼此提升，但实际训练还需要选择合适的目标函数和参数，可能不稳定。

**历史意义：**它代表了深度学习生成模型的一条重要路线，补足只按图像识别叙述发展史的偏差。

[来源：NeurIPS 2014 论文](https://proceedings.neurips.cc/paper/2014/hash/f033ed80deb0234979a61f95710dbe25-Abstract.html)

[论文库介绍：B04 · GAN](paperweb/paper.html?id=B04)

### 2015（会议发表于 2016）· ResNet

Kaiming He、Xiangyu Zhang、Shaoqing Ren 与 Jian Sun 提出残差学习框架。普通网络要让每一层都学习新的变换；ResNet 则通过“捷径连接”把较早层的信息直接送到较后层，让后面的层重点学习在已有信息上需要增加的变化。这种设计有助于训练更深的网络。团队的系统在 ILSVRC 2015 分类任务中取得第一名，论文随后发表于 CVPR 2016。

**历史意义：**它展示了网络结构改进如何缓解深层网络优化困难，也提醒读者区分竞赛年份与论文正式发表年份。

[来源：CVF Open Access 论文页](https://openaccess.thecvf.com/content_cvpr_2016/html/He_Deep_Residual_Learning_CVPR_2016_paper.html)

[论文库介绍：B08 · ResNet](paperweb/paper.html?id=B08)

### 2016 · AlphaGo 将深度学习用于围棋

David Silver 等人在 *Nature* 发表 AlphaGo 研究，介绍如何结合深度神经网络与蒙特卡洛树搜索来选择围棋落子。一个网络估计哪些落子值得考虑，另一个网络评估局面和胜率，搜索程序再比较可能的后续走法。论文报告 AlphaGo 在 2015 年与欧洲围棋冠军 Fan Hui 的比赛中以 5 比 0 获胜。围棋的局面组合极多，这项成果展示了学习模型与搜索方法结合的力量。

**历史意义：**它让深度学习的影响从图像识别扩展到复杂策略决策，也是理解强化学习、搜索与神经网络如何协同工作的代表案例。

[来源：*Nature* 原始论文](https://doi.org/10.1038/nature16961)

[论文库介绍：B06 · AlphaGo](paperweb/paper.html?id=B06)

</div>

## Transformer 与生成式模型扩展 · 2017—至今

Transformer 最初针对序列转换任务提出，随后成为多种预训练语言模型的重要架构基础。生成式 AI 的发展还包含训练规模、数据、对齐方法、扩散模型和产品化等多条路线，不能简化为某一篇论文的线性结果。

<div class="ai-timeline__events" markdown>

### 2017 · Transformer

Vaswani 等人在 NeurIPS 发表 *Attention Is All You Need*。当模型处理一句话时，注意力机制会计算不同词语之间的关联，让模型在处理某个词时参考句子中其他相关位置的信息。论文据此提出 Transformer：不使用传统的循环结构或卷积结构来处理序列，并在机器翻译任务中报告实验结果。论文提出的是一种架构，并没有直接研究后来聊天机器人具备的全部能力。

**历史意义：**它是现代语言模型发展脉络中的关键架构论文之一。原论文的实验范围是机器翻译等任务，不应把后来的大语言模型能力倒推为该论文当时已经实现。

[来源：NeurIPS 论文](https://proceedings.neurips.cc/paper_files/paper/2017/hash/3f5ee243547dee91fbd053c1c4a845aa-Abstract.html)

[论文库介绍：B09 · Transformer](paperweb/paper.html?id=B09)

### 2020 · GPT-3 与少样本学习

Brown 等人在 NeurIPS 发表 GPT-3 研究。GPT-3 根据前文逐个预测下一个词（或词元），再把预测结果接回文本继续生成。论文展示了一种“上下文学习”方式：给模型一段任务说明和几个示例，不重新训练或更新模型参数，就让它尝试完成新例子。实验表明模型规模与这类表现有关，但结果会随任务而变化，也不代表模型真正理解或总能给出正确答案。

**历史意义：**它把“规模扩大与上下文示例”带来的少样本能力作为重要研究现象展示出来；论文也明确讨论了模型仍会失败及数据方法上的问题。

[来源：NeurIPS 2020 论文](https://proceedings.neurips.cc/paper/2020/hash/1457c0d6bfcb4967418bfb8ac142f64a-Abstract.html)

[论文库介绍：B11 · GPT-3](paperweb/paper.html?id=B11)

### 2020 · 扩散生成模型

Ho、Jain 与 Abbeel 的 *Denoising Diffusion Probabilistic Models* 研究一种逐步生成图像的方法。训练时，模型先学习如何把图像一点点加上随机噪声；生成时则从随机噪声开始，反复预测并去除噪声，最终得到图像。论文在图像生成实验中报告了结果。这种方法的直观特点是生成过程分成许多小步，而不是一次直接画出完整图像。

**历史意义：**它代表与自回归模型、GAN 不同的生成建模路线，帮助时间线覆盖多种生成方法。

[来源：NeurIPS 2020 论文](https://proceedings.neurips.cc/paper/2020/file/4c5bcfec8584af0d967f1ab10179ca4b-Abstract.html)

[论文库介绍：F12 · DDPM](paperweb/paper.html?id=F12)

### 2022 · ChatGPT 研究预览发布

OpenAI 于 2022 年 11 月 30 日发布 ChatGPT 研究预览。这是一个可以通过多轮文字对话回答问题、改写文本和协助完成任务的产品服务，不是当日发表的一篇研究论文。发布说明称其训练使用了人类反馈强化学习：人类评估者比较模型回答，反馈被用于进一步调整模型。对话形式让公众更容易试用生成式模型，同时也暴露出回答不准确等问题。

**历史意义：**这是生成式 AI 面向公众产品化的重要时间点，属于产品发布事件，不是学术论文发表节点。

[来源：OpenAI 发布说明](https://openai.com/index/chatgpt/)

[论文库介绍：B14 · InstructGPT（RLHF 技术背景）](paperweb/paper.html?id=B14)

### 2023 · GPT-4 发布

OpenAI 于 2023 年 3 月发布 GPT-4。官方材料称它能接收文本和图像输入，并生成文本输出；“多模态”指模型处理不止一种形式的信息。发布材料还包括研究介绍和系统卡，描述评测结果、已知限制及安全工作。读者应把这些描述理解为特定测试和使用条件下的报告，而不是对所有任务都正确或可靠的保证。

**历史意义：**它展示了大型生成模型能力评估与安全说明逐渐成为公开发布材料的一部分。能力描述应以官方报告的测试范围和限制为准。

[来源：OpenAI GPT-4 研究介绍](https://openai.com/index/gpt-4-research/)

[论文库介绍：B15 · GPT-4](paperweb/paper.html?id=B15)

</div>

</div>

## 分期和选目说明

- 这里的时期是为学生阅读而设的**编辑性分组**，不是由某个机构正式发布的唯一 AI 历史分期。权威资料用于核验节点事实，不被拿来伪装成对分期的背书。
- 节点优先选择可由原始论文、正式会议/期刊记录、奖项机构或专业博物馆资料核验的成果；竞赛结果引用论文或竞赛相关正式来源。
- 代表性不以引用量单独决定。页面优先解释方法贡献、实验结果或历史语境；若增加引用量，应注明数据库和查询日期。
- 论文年份按正式发表年份；若节点同时涉及更早竞赛结果或预印本，会在文案中说明。产品发布单独标为事件，不混入论文发表年份。
- 资料初查日期：2026-10-21。后续维护如改变节点或分期，应同步更新此页来源与说明。

## 主要参考机构与论文来源

- [Nature：Learning representations by back-propagating errors（1986）](https://doi.org/10.1038/323533a0)
- [Oxford Academic：Computing Machinery and Intelligence（1950）](https://doi.org/10.1093/mind/LIX.236.433)
- [诺贝尔奖：2024 年物理学奖背景资料](https://www.nobelprize.org/prizes/physics/2024/popular-information/)
- [Computer History Museum：AI & Robotics 时间线](https://www.computerhistory.org/timeline/ai-robotics/)
- [Computer History Museum：Chatbots Decoded](https://computerhistory.org/stories/chatbots-decoded/)
- [MIT Press：*Perceptrons*（1969）](https://mitpress.mit.edu/9780262130431/perceptrons/)
- [NeurIPS：AlexNet（2012）](https://proceedings.neurips.cc/paper/2012/hash/c399862d3b9d6b76c8436e924a68c45b-Abstract.html)
- [IEEE：Gradient-Based Learning Applied to Document Recognition（1998）](https://doi.org/10.1109/5.726791)
- [Science：Reducing the Dimensionality of Data with Neural Networks（2006）](https://doi.org/10.1126/science.1127647)
- [Nature：Mastering the game of Go with deep neural networks and tree search（2016）](https://doi.org/10.1038/nature16961)
- [NeurIPS：Generative Adversarial Nets（2014）](https://proceedings.neurips.cc/paper/2014/hash/f033ed80deb0234979a61f95710dbe25-Abstract.html)
- [CVF：ResNet（CVPR 2016）](https://openaccess.thecvf.com/content_cvpr_2016/html/He_Deep_Residual_Learning_CVPR_2016_paper.html)
- [NeurIPS：Attention Is All You Need（2017）](https://proceedings.neurips.cc/paper_files/paper/2017/hash/3f5ee243547dee91fbd053c1c4a845aa-Abstract.html)
- [NeurIPS：Language Models are Few-Shot Learners（2020）](https://proceedings.neurips.cc/paper/2020/hash/1457c0d6bfcb4967418bfb8ac142f64a-Abstract.html)
- [NeurIPS：Denoising Diffusion Probabilistic Models（2020）](https://proceedings.neurips.cc/paper/2020/file/4c5bcfec8584af0d967f1ab10179ca4b-Abstract.html)
- [OpenAI：ChatGPT 发布说明（2022）](https://openai.com/index/chatgpt/)
- [OpenAI：GPT-4 研究介绍（2023）](https://openai.com/index/gpt-4-research/)
