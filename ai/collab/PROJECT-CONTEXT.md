# 项目上下文（慢变）

## 仓库

- 名称：HZCU 学生宝典（MkDocs Material）
- 路径：`C:\Users\pc\Documents\GitHub\hzcu-student-handbook`
- 线上：`https://hzcu-pc.github.io/hzcu-student-handbook/`
- 当前分支：`main`（本地有大量未提交改动，论文页扩到 205 篇）

## 你负责的范围

- **论文浏览页：** `docs/papers.md` + `docs/javascripts/papers-shelf.js` + `docs/stylesheets/papers-workbench.css`
- **时间线深链：** `docs/ai-timeline.md`

## P0 问题摘要

### P0-1 HTML 结构

`#empty` 误在 `#grid` 内 → `grid.innerHTML = ''` 删掉 empty → JS 报错 → 深链不执行。

### P0-2 时间线深链映射（旧 id → 新 id）

| 时间线标签 | 链接应使用 |
|---|---|
| 反向传播 | `papers.md?id=WB-A01&from=ai-timeline` |
| LeNet-5 | `WB-B01` |
| AlexNet | `WB-B02` |
| GAN | `WB-E01` |
| ResNet | `WB-B05` |
| AlphaGo | `WB-D02` |
| Transformer | `WB-A09` |
| GPT-3 | `WB-A12` |
| DDPM | `WB-E03` |
| InstructGPT | `WB-A22` |
| GPT-4 | `WB-A26` |

不能对旧 `B01` 简单加 `WB-` 前缀（旧 B01=反向传播，新 WB-B01=LeNet-5）。

### P0-3 双份 JS

`papers.md` 内联脚本 + `mkdocs.yml` 的 `extra_javascript` → 双 init；外部脚本需在无 `#papers-json` 时 early return。

## P1 数据债（P0 后再动）

- 156/205 模板句 `solve`；authors/venue/link 占位；重复条目 LLaMA/Mamba；卡片与 JSON citations 不一致
- `scripts/.paper_rewrite_progress.json` 的 `completed` **不可信**（实际只完成少量 batch）

## 分工提醒

- Cursor：改稿、merge、regenerate
- **Codex：P1-a 扩写 batch（主）** — 遵守 `P1-VOICE.md`，不规定句式
- DSH：构建 + 校验，**不写** `papers.md`
- WorkBuddy：**P1-c 等元数据**（CUR 另派时）；非默认扩写
