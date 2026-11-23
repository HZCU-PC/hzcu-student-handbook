# CUR · 合并 P1-gen（regenerate_paper_cards）

**时间：** 2026-11-04 00:38  
**依据：** `logs/2026-11-04-0035-codex-p1-gen.md`

## 操作

1. `regenerate_paper_cards.py --check` → 205 卡 / 205 shot / changed  
2. 备份 `backups/papers-pre-regen.bak`；移出 `docs/papers.md.bak` → `backups/papers-pre-gen.bak`（避免 mkdocs 复制进站点）  
3. 因直接 `write_text(papers.md)` 报 `OSError 22`，改用 `papers.gen.tmp` 生成后 **替换** `docs/papers.md`  
4. CUR 小补：`regenerate_paper_cards.py` 恢复 `crank>=4` → `cite hot`（CDX 原版仅 `cite`）

## 验收

```
p1_audit   citation_mismatch 0, dual 0, duplicate_badge_cards 0
shotimg    39（与合并前一致）
mkdocs --strict  PASS
```

## 状态

- **P1-gen：** 完成 ✓  
- **WKB：** **解冻** — 内容阶段：只 patch JSON + batch 脚本，合并后 **必须** `regenerate_paper_cards.py`  
- **请 DSH V-3**（结构 regenerate + 三项 badge 指标）

## 锁

**已释放**
