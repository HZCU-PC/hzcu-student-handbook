# P1-b · 重复条目方案（待 WKB / 用户确认）

## LLaMA（2 条）

| id | year | org | hook 摘要 | 建议 |
|---|---|---|---|---|
| **WB-A23** | 2023 | Meta AI | 可私有化基础设施 | **保留** — 对应 LLaMA 1 论文 |
| **WB-A52** | 2025 | Meta AI | 同 A23 文案 | **需改** — 应为 LLaMA 3/4 或独立论文；勿与 A23 同 `zh` |

**WKB 结论（2026-11-03）：选 1，改名保留，勿删。**

- 真实身份：**Llama 4**（Meta，2025-04-06 官方发布，**无正式论文**）。
  佐证：A52 的 `rel` 已标 `WB-A33（Llama 3）=前身`、`WB-A41=相关`，与 Llama 4 完全吻合；删除会牵连 rel 与 205 计数。
- 建议字段（完整值见 `logs/2026-11-03-2356-wkb-batch03.md` 与 `scripts/batch03_wkb_draft.py` 的 `RENAME` 段）：
  - `zh`: `Llama 4`；`en`: `The Llama 4 herd: Scout, Maverick, and Behemoth（Meta 官方发布说明）`
  - `venue`: `官方发布说明 · 无正式论文`；`link`: `https://ai.meta.com/blog/llama-4-multimodal-intelligence/`
  - `authors`: `Meta AI（Llama 团队）`；`hook`: `Llama 首次 MoE 化＋原生多模态，上下文号称 10M`
  - `solve/method/impact/tags` 新文案见批次文件（含「发布翻车/特调争议，以第三方复现为准」的口径）。
- **CUR 注意**：卡片 `h3`/`aria-label` 与 `<small>` 需同步改名；`citations` 建议降为 `<1千`（已是）。

## Mamba（2 条）

| id | year | org | 建议 |
|---|---|---|---|
| **WB-A35** | 2024 | CMU | **保留** — Mamba SSM 原论文 |
| **WB-A50** | 2025 | MiniMax | **需改标题** — 与 A35 同 `zh`「Mamba」不合理；应为 MiniMax 实际论文名 |

**WKB 结论（2026-11-03）：改名保留，勿删。**

- 真实身份：**MiniMax-01**（MiniMax，2025-01-15，arXiv:2501.08313）。
  佐证：A50 现有 hook「把注意力的二次复杂度改成线性」正是 Lightning Attention 的定位；`org=MiniMax / year=2025` 与该论文一致；`rel` 中 `WB-A34（Mixtral，MoE）=相关` 亦合理（MiniMax-01 为 MoE＋线性注意力）。
- 建议字段（完整值同上批次文件）：
  - `zh`: `MiniMax-01`；`en`: `MiniMax-01: Scaling Foundation Models with Lightning Attention`
  - `venue`: `arXiv 预印本`；`link`: `https://arxiv.org/abs/2501.08313`（DOI: `10.48550/arXiv.2501.08313`）
  - `authors`: `MiniMax（Aonian Li、Bangwei Gong、Yiran Zhong 等）`
  - `tags` 中 `预印本 2023` → `预印本 2025`；`hook` 保留原文案（恰好贴切）。
- **CUR 注意**：卡片 `h3`/`aria-label` 同步改为 MiniMax-01；正文 solve/method/impact 用批次文件新文案替换。

## 执行顺序

1. WKB 在本文件或 log 中填最终标题 + 是否删条目。  
2. CUR 单次持锁改 `papers.md`。  
3. DSH V-2 复查 id 唯一与 205 计数。
