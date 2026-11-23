# 协作日志说明

每次有 Agent **写文档**或**改仓库**，在本目录新增一个文件，不要覆盖旧日志。

## 命名

```text
YYYY-MM-DD-HHMM-<角色>-<主题>.md
```

示例：`2026-11-03-2325-cursor-p0-fix.md`

角色：`cursor` | `dsh` | `chatgpt` | `workbuddy` | `user`

## 正文模板

```markdown
# <主题>

- **角色：** Cursor
- **时间：** 2026-11-03 23:25
- **读了：** ai/collab/PLAN.md, LOCK.md, …
- **LOCK：** 已占用 / 已释放 — docs/papers.md

## 做了什么

（ prose 或 bullet）

## 改了哪些文件

| 文件 | 变更摘要 |
|---|---|
| docs/papers.md | … |

## 如何验收

1. …

## 下一步

请 DSH 验证 / 请用户浏览器点检 / 请 ChatGPT 更新 PLAN
```

## 与 outbox/ 的关系

- **logs/**：完整记录，按时间归档，**权威历史**。
- **outbox/<角色>/latest.md**：可选，只保留该角色最新状态，方便快速打开。
