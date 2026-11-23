# CUR → CDX：P1-gen 已汇总关单 · 新派单 batch04

**时间：** 2026-11-04 00:46  
**给：** Codex 窗口若仍显示「P1-gen 请 CUR 汇总」——**那一棒已结束**，勿重复交付 regenerate。

---

## 已汇总（不必再做）

| 项 | 状态 | 证据 |
|---|---|---|
| P1-gen `regenerate_paper_cards.py` | ✅ CUR 已 merge | `logs/2026-11-04-0038-cursor-merge-p1-gen.md` |
| P1-cit + P1-d | ✅ 已 merge | `logs/2026-11-04-0018-cursor-merge-citfix-p1d.md` |
| DSH V-3 | ✅ 通过 | `logs/2026-11-04-0033-dsh-verify-v3.md` |

**你不需要**再写 P1-gen 日志或请 CUR 合并 regenerate。

---

## 当前 CDX 派单（请读最新 `DISPATCH.md`）

**任务 ID：P1-a · batch04**（扩写主责，用户 2026-11-04 定调）

1. 写 `scripts/batch04_cdx.py` — `CONTENT` 字典，patch `#papers-json` 的 solve/method/impact/hook（15～20 篇，优先仍模板的 WB-B* / WB-D* / WB-F*，勿与 batch03 id 重复）  
2. 语气：**`expand_paper_explanations.py` 的 B02/B03**（类比 + plain + 局限）；结构参考 `batch03_wkb_draft.py`  
3. 写 `logs/*-codex-batch04.md`，末尾 **请 CUR 汇总**  
4. **禁止**改 `docs/papers.md`

CUR 收到后会：持锁 → 跑 batch 脚本 → `regenerate_paper_cards.py` → audit。

---

## 一句话给 Codex

> P1-gen 已合并关单。新任务是 **P1-a batch04 扩写**，见 `DISPATCH.md` 与 `prompts/codex.md`，交付 `batch04_cdx.py` + log。
