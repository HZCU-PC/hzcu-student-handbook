# CUR · DSH 抽验回应（三项硬修）

**时间：** 2026-11-04  
**依据：** DSH 对 batch05–07 合并后的书面抽验（用户转发；DSH 未改仓库文件）

## 已做

### 1. 备份不再进 `docs/` / 站点

- `regenerate_paper_cards.py`：备份改为 `backups/papers.md.gen.bak`
- 已移走 `docs/papers.md.gen.bak`
- `.gitignore`：`docs/*.bak`、`site-test/`（构建产物）

### 2. 版本点（见 git commit，本条写于提交前）

- 拟提交：`docs/`、`scripts/`（batch/regenerate/audit 等）、`ai/collab/`、`backups/`、`.gitignore`

### 3. audit 内容下限

- `thin_content`：`solve`/`method`/`impact` 任一 **<60 字** → 当前 **43** 篇（含部分早期短文，非全是空洞）
- `placeholder_prose`：含 workbook 填充套话 → **7** 篇，与 DSH 列表一致：  
  `A41 A48 A53 B21 C04 D16 G01`  
- CLI：`--thin`、`--placeholder`

## 未在本轮改（记录债）

- **7 篇空洞**：不含「核心问题，是如何」，批次守卫选不中 → 需 **专批**（非 batch08 模板流）
- **hook 与卡片标题**：10×「基座模型 · 语言」等 → 待 hook 同步或 regenerate 默认规则
- **P1-VOICE 下限文案**：可另开 `P1-QUALITY.md` 与 audit 对齐
- **batch08**：模板 54 篇仍按 DISPATCH；空洞 7 篇 CUR 将单列 id

## 核验

- `p1_audit.py`：`placeholder_prose` **7**
- `mkdocs --strict` → `site-test` 无 `papers.md.gen.bak`
