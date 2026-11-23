# CUR · hook 去重（一批）

**时间：** 2026-11-04  
**脚本：** `scripts/batch_hook_dedupe_cur.py`（仅 JSON `hook`，守卫：当前 hook 必须等于待替换的重复标签）

## 本批 32 篇

| 原重复 hook | 篇数 |
|---|---|
| 基座模型 · 语言 | 9 |
| 数据与基准 · 语言 | 14 |
| 应用系统 · 科学 | 6 |
| 新架构 · 视觉 | 3 |

## 结果

- regenerate 后卡片 `<p class="hook">` 已更新
- `template_hook`：49 → **17**
- 重复 hook 字符串组：**10 → 6**（余：应用系统·语言×3、新架构·语言×3 等，下批可继续）
- `p1_audit` 新增 `duplicate_hook_groups` / `max_hook_collision`

## 合并

`batch_hook_dedupe_cur.py` → regenerate → audit → strict **PASS**
