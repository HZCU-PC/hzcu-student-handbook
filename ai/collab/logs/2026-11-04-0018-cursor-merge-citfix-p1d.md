# CUR · 合并 CDX P1-cit-fix + P1-d（expand）

**时间：** 2026-11-04 00:18  
**依据：** `logs/2026-11-04-0013-cdx-citfix-p1d.md`、`outbox/codex/latest.md`  
**备份：** `docs/papers.md.bak`

## 对「只改 .cite」偏离的裁决

**同意（非否掉）。** 理由：

- CUR 原意是 **不插入元素、修用户可见角标**；61 张占位卡只有 `<small>`，只改 `.cite` 无法归零。
- CDX 方案：**有 cite → 改 cite + 删重复 small**；**无 cite → 改唯一 small**；`&lt;1千` 转义属规范化，渲染不变。
- 与「绝不插入」一致，且修前 audit **100** / dual **39** → 修后 **0** / **0**。

## 执行命令与输出

```text
p1_audit（修前）     citation_mismatch 100, dual_badge_cards 39
p1_sync --check      cite 39 + small 135 + 删 small 39
p1_sync（实跑）      已写入 papers.md
p1_audit --mismatch  （无行）
expand main()        扫描 205，扩展 44 篇（JSON 区块）
p1_audit（后）       citation_mismatch 0, dual 0, template_solve 140
mkdocs --strict      PASS（0.51s）
```

## 状态

- **P1-cit-fix：** 已合并 ✓  
- **P1-d（expand merge）：** 已合并 ✓（与 WKB batch 分开授权，本次用户明示合并）

## 锁

**已释放**

---

**请 DSH 验证 V-2**（strict + `p1_audit.py` + 抽查有图卡角标与占位卡 `&lt;1千` 渲染）
