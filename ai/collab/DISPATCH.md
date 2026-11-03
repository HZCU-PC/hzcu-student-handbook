# 当前派单（总调度：CUR）

> **最后更新：** 2026-11-04 03:20 · **P1-a 模板扩写已清零**

## 状态板

| 代号 | 状态 | 任务 |
|---|---|---|
| **CDX** | ✅ | P1-a 批次完成 |
| **WKB** | 🟡 | **P1-c**：authors / 正式 link（92+92） |
| **CUR** | — | hook 余债（6 template_hook、1 duplicate 组）可选 |
| DSH | 建议 | batch10 后全量 spot-check |

## audit

- **template_solve 0** · template_hook **6** · badge **0**
- placeholder_prose **0** · duplicate_hook_groups **1**
- placeholder_authors **92** · arxiv_search_link **92**
- thin_content **72**（<60 字/字段，可选后续加长）
- batch10：`logs/2026-11-04-0320-cursor-merge-batch10.md`

---

## WKB · P1-c（元数据）

- 替换「作者信息见原论文」
- arxiv.org/search → 正式 DOI / arXiv abs
- 交付脚本或 CSV + log；**请 CUR 汇总**（若改 JSON 字段）

---

## 可选 · hook 第三批

余 **6** 条 `字段 · 类型` 式 hook + **1** 组重复 — 扩 `batch_hook_dedupe_cur.py`
