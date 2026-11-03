# P1-gen · 卡片 HTML 由 JSON 生成（规格）

> **用户决策（2026-11-04）：** 先改结构、后填内容。P1-gen **阻塞** WKB batch04 / P1-c，直至 CUR 合并 regenerate 并通过 DSH V-3。

## 目标

`docs/papers.md` 内 **唯一事实来源** = `<script id="papers-json">`。  
`#grid` 内 205 个 `<article class="card">` **由脚本生成**，避免 JSON 与列表双写。

## 非目标（本版不做）

- 不把 JSON 拆出到独立文件（可后续 P2）
- 不重编码 / 不删除现有 base64 截图（**按 id 原样保留** `.shot` 内 HTML）
- 不改 sidebar / bar / empty / scrim / sheet 壳层

## 脚本（CDX 交付）

建议路径：`scripts/regenerate_paper_cards.py`

### 输入 / 输出

1. 读 `docs/papers.md`
2. 解析 `#papers-json` → `List[Paper]`（顺序 = 卡片顺序）
3. 从**当前**文件中按 `data-id` 抽取 `.shot` 内层 HTML → `shots[id]`（缺失则占位模板）
4. 替换 `#grid` 与 `</div><!-- grid? -->` 之间全部 `<article>...</article>` 为新生成块
5. **不修改** JSON 脚本块字节（除非 `--also-json` 未启用时只动 grid）

CLI：

```text
python scripts/regenerate_paper_cards.py --check   # diff 统计，不写盘
python scripts/regenerate_paper_cards.py           # 写 papers.md（CUR 持锁）
```

### 每卡生成字段（来自 JSON）

| 输出 | JSON 字段 | 备注 |
|---|---|---|
| `data-id` | `id` | |
| `data-field` | `field` | |
| `data-kind` | `kind` | |
| `data-country` | `country` | |
| `data-org` | `org` | |
| `data-year` | `year` | |
| `aria-label` | `zh` | HTML 转义 |
| `<h3>` | `zh` | |
| `<p class="hook">` | `hook` | 缺省可 `field · kind` |
| `.shot` 内角标 | `citations` | 见下 |
| `.tags` | `tags[]` + `field` 色 | 与现有 class 一致 |
| `.cmeta` | `org` | 保持 `<span class="dot">·</span>` 结构 |

### 角标规则（与 `p1_sync_citations.py` / audit 一致）

- 有 `<img class="shotimg">` 的 shot：角标为  
  `<span class="cite[ hot]">…</span>`（`hot` 规则：`crank >= 4` 或与现网 12 张一致，CDX 实现时对照现文件统计）
- 占位 `paper-placeholder`：角标为 `<small>…</small>`，文本用 `esc_badge(citations)`（`<` → `&lt;`）
- **禁止** 同时出现 cite + small

### 占位 shot 模板

无 preserved shot 且无 img 时：

```html
<div class="shot paper-placeholder"><span>{number 或 id 后缀}</span><small>{citations escaped}</small></div>
```

### 验收（CDX 在 temp 副本上）

- 205 articles，id 顺序与 JSON 一致
- `p1_audit.py`：`citation_mismatch 0`，`dual_badge_cards 0`
- `papers-shelf.js`：`SHOT` 缓存仍可用（每卡仍有 `.shot`）
- `mkdocs build --strict` PASS
- 抽样：有图卡 cite 可见；占位卡 small 可见

## CUR 合并流程

1. CDX log + `--check` 输出  
2. CUR 持锁：`Copy-Item papers.md.bak` → `regenerate_paper_cards.py`  
3. audit + mkdocs  
4. **请 DSH V-3**（结构变更）  
5. 解冻 WKB：**P1 内容阶段**（batch04 / expand / P1-c）

## WKB 冻结说明

gen 完成前：**不要** 新建会 patch `docs/papers.md` 的 batch；可只读、可写 logs 规格。
