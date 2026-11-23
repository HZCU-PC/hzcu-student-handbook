# CUR · merge batch06（CDX）

**时间：** 2026-11-04 01:30（Asia/Shanghai）  
**上游：** `logs/2026-11-04-0120-codex-batch06.md`、`scripts/batch06_cdx.py`

## 合并步骤

1. `LOCK.md` → 占用  
2. 备份 `backups/papers-pre-batch06.bak`  
3. `python scripts/batch06_cdx.py` → **18 JSON patches**  
4. `python scripts/regenerate_paper_cards.py` → 205 卡，changed=True  
5. `python scripts/p1_audit.py`  
6. `mkdocs build -d site-test --strict` → **PASS**  
7. `LOCK.md` → 空闲  

## audit

| 指标 | batch05 后 → batch06 后 |
|---|---|
| template_solve | 90 → **72** |
| template_hook | 80 → **67** |
| citation_mismatch | 0 |
| dual / duplicate badge | 0 |

## 篇目（CDX 18）

WB-A44, A54, A55 · B19, B24–B31 · C11, C14 · E05–E07 · D10

## 备注

- CDX 日志：部分条目仍为题名检索链接，正式来源可后续 P1-c / 人工核元数据。  
- 下一批：**batch07**（18 篇）已写入 `DISPATCH.md`。
