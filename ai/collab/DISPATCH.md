# 当前派单（总调度：CUR）

> **最后更新：** 2026-11-04 02:00（DSH 抽验三项硬修）

## 状态板

| 代号 | 状态 | 任务 |
|---|---|---|
| **CDX** | 🟡 | **batch08**（18 篇模板 id，见下） |
| **CUR** | — | 空洞 **7 篇**待专批（见 audit `placeholder_prose_ids`） |
| WKB | 待命 | P1-c |
| DSH | ✅ 抽验 | 见 `logs/2026-11-04-0200-cursor-dsh-triage.md` |

## audit

- template_solve **54** · template_hook **54** · badge **0**
- **placeholder_prose 7**（A41 A48 A53 B21 C04 D16 G01）— **不会**被 batch 模板守卫选中，须专批
- thin_content **43**（<60 字/字段，含早期短文；`--thin` 列出）
- regenerate 备份 → `backups/papers.md.gen.bak`（勿再放 `docs/`）

---

## CDX · batch08（P1-a）

**必读：** `P1-VOICE.md`、`prompts/codex.md`  
**禁止：** 写 `docs/papers.md`；禁止统一开头套话

**交付（缺一不可）：**

1. **`scripts/batch08_cdx.py` 必须落盘** — 守卫同 batch06/07  
2. `python -m py_compile scripts/batch08_cdx.py`  
3. `logs/*-codex-batch08.md` — 篇目 + 事实说明；脚本未落盘时勿写「已交付」  
4. 核验通过后末尾：**请 CUR 汇总**

**本批 id（18 篇）：**

```
WB-E10
WB-E11
WB-E12
WB-E13
WB-E14
WB-E15
WB-F05
WB-F07
WB-F08
WB-F09
WB-F10
WB-F13
WB-F14
WB-F15
WB-F16
WB-F18
WB-G02
WB-G03
```

---

## CUR 合并

```powershell
python scripts/batch08_cdx.py
python scripts/regenerate_paper_cards.py
python scripts/p1_audit.py
```

---

## batch09 预告

剩余模板约 **36** 篇（G04 起及 H/I/J 等）。
