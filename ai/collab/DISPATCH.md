# 当前派单（总调度：CUR）

> **最后更新：** 2026-11-04 02:35

## 状态板

| 代号 | 状态 | 任务 |
|---|---|---|
| **CDX** | 🟡 | **batch09**（18 篇，见下） |
| **CUR** | 待命 | CDX 交付后 merge |
| WKB | 待命 | P1-c |
| DSH | spot-check | 合并后可抽验 |

## audit

- template_solve **36** · template_hook **15** · badge **0** · duplicate_hook_groups **5**
- placeholder_prose **0**
- batch08 已 merge：`logs/2026-11-04-0235-cursor-merge-batch08.md`

---

## CDX · batch09（P1-a）

**必读：** `P1-VOICE.md` · **交付：** `scripts/batch09_cdx.py` 落盘 + compile + log · **请 CUR 汇总**

**本批 id（18 篇）：**

```
WB-G04
WB-G05
WB-G07
WB-G08
WB-G09
WB-G10
WB-G11
WB-G12
WB-G13
WB-G14
WB-G15
WB-G16
WB-H01
WB-H02
WB-H03
WB-H05
WB-H06
WB-H07
```

---

## CUR 合并

```powershell
python scripts/batch09_cdx.py
python scripts/regenerate_paper_cards.py
python scripts/p1_audit.py
```

---

## batch10 预告

剩余模板 **18** 篇：H08 起及 I/J 轨道（跑 `_list_tpl` 确认）。
