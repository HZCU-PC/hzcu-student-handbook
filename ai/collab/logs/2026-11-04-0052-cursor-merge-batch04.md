# CUR · 汇总 batch04（CDX + WKB）

**时间：** 2026-11-04 00:52  
**触发：** 用户「请 CUR 汇总」+ CDX log `0110-codex-batch04`（并行合并 WKB `0039-wkb-batch04`，id 无重叠）

## 合并

| 脚本 | 篇数 | 范围 |
|---|---|---|
| `batch04_wkb_draft.py` | 16 | A29–A45 国产基座 + A35 Mamba + B05–B20 视觉 |
| `batch04_cdx.py` | 16 | D01–D22 决策 + F03–F17 科学 |

备份：`backups/papers-pre-batch04.bak`

```text
batch04 WKB 16 + CDX 16 → regenerate → audit → mkdocs --strict PASS
```

## audit 变化

| 指标 | 合并前 | 合并后 |
|---|---|---|
| template_solve | 140 | **108** |
| template_hook | 116 | **89** |
| citation / dual / duplicate | 0 | 0 |
| papers / cards | 205 | 205 |

## 锁

**已释放**

---

WKB 下一批候选见其 log。**请 DSH** 可选 spot-check（不必全量 V-3）。
