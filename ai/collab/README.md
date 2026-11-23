# 多 Agent 协作目录（hzcu-student-handbook）

本文件夹是 **四人编组** 的**唯一异步信箱**：**CUR（Cursor·总调度）、CDX（Codex）、DSH（DeepSeek Harness）、WKB（WorkBuddy）**。它们不能互相聊天，只读 **`DISPATCH.md`** 派单；**人类用户负责转发一句「看 DISPATCH」**。

仓库路径：

`C:\Users\pc\Documents\GitHub\hzcu-student-handbook\ai\collab\`

---

## 这个文件夹是干什么的

| 作用 | 说明 |
|---|---|
| **写** | 每个 Agent 把计划、进度、验证结果、疑问写进 `logs/` 或 `outbox/<角色>/` |
| **改** | **只有 Cursor / WorkBuddy 在持有锁时** 才能改仓库里的源码；改完必须在日志里列出文件与摘要 |
| **读** | 任何 Agent 开始工作前必须先读：`README.md`、`ROSTER.md`、**`DISPATCH.md`**、`LOCK.md`、`PLAN.md`、`PROJECT-CONTEXT.md` |
| **防覆盖** | `LOCK.md` 标明谁正在独占哪些路径（尤其 `docs/papers.md`，约 1.7 MB） |

不要把聊天历史当真相；**以本目录最新文件 + git diff 为准**。

---

## 目录结构

```text
ai/collab/
├── README.md              ← 协作规则（本文件）
├── ROSTER.md              ← 四人代号与职责（CUR/CDX/DSH/WKB）
├── DISPATCH.md            ← **总调度派单板**（当前谁干什么）
├── LOCK.md                ← 当前文件锁（改仓库前必看）
├── PLAN.md                ← 冲刺任务与验收（CUR 维护状态）
├── PROJECT-CONTEXT.md     ← 项目背景、P0/P1 问题清单（慢变）
├── prompts/               ← 复制给其他 AI 的启动 Prompt
│   ├── 粘贴给任意AI.md
│   ├── cursor.md          ← CUR 总调度
│   ├── codex.md           ← CDX
│   ├── dsh.md             ← DSH
│   └── workbuddy.md       ← WKB
├── logs/                  ← 按时间记录「写了什么、改了什么」
│   └── YYYY-MM-DD-HHMM-<角色>-<主题>.md
├── outbox/                ← 各角色最新状态（可选，与 logs 二选一或并用）
│   ├── cursor/
│   ├── codex/
│   ├── dsh/
│   └── workbuddy/
└── archive/               ← 从外部 handoff 迁入的旧文档，只读参考
```

---

## 角色分工（四人编组）

详见 **`ROSTER.md`**。摘要：

| 代号 | 负责 | 禁止 |
|---|---|---|
| **CUR** | 总调度、`DISPATCH.md`、占锁、改 `papers.md` / 时间线、汇总 logs | 未验证就宣称上线 |
| **CDX** | CUR 派单：JS/CSS、脚本、PLAN 细化 | 自派单；写 `papers.md` |
| **DSH** | 构建 + 数据校验报告 | 写 `docs/` |
| **WKB** | CUR 派单：P1 内容流水线、`scripts/` | P0 期间动锁定路径 |
| **用户** | 转发 DISPATCH、批准开工 | — |

---

## 单次协作流程

1. **读** `LOCK.md` — 若有人锁定，只读不改被锁路径。
2. **读** `PLAN.md` + `PROJECT-CONTEXT.md` — 确认当前任务。
3. **需要改仓库时** — 更新 `LOCK.md`（谁、哪些文件、预计何时释放）。
4. **干活** — 在仓库内修改（或只写文档）。
5. **写日志** — 在 `logs/` 新建一条，格式见 `logs/README.md`。
6. **释放锁** — 清空或更新 `LOCK.md`；若完成 P0/P1，在日志里写 **「请 DSH 验证」** 或 **「请用户验收」**。

---

## 构建与验证（DSH 专用命令）

在仓库根目录：

```powershell
cd C:\Users\pc\Documents\GitHub\hzcu-student-handbook
.\.venv\Scripts\python.exe -m mkdocs build -f mkdocs.yml -d site-test --strict
```

验证结论写入：`logs/YYYY-MM-DD-HHMM-dsh-verify-<主题>.md`

---

## 与旧 handoff 的关系

DSH scratch 目录 `_scratch/hzcu-handoff/` 中的 `AGENT-NOTE-for-cursor.md`、`worktree.patch` 等已汇总进 `PROJECT-CONTEXT.md` 与 `archive/`。**以后以 `ai/collab/` 为准**。

---

## 给用户的最短用法

1. 打开 **`DISPATCH.md`** 看当前派单。
2. 把 `prompts/<角色>.md` 复制到 Codex / DSH / WorkBuddy；告诉 Cursor：「按 DISPATCH 执行」。
3. 各 Agent 只写 `logs/`；**只有 CUR 改 DISPATCH 与 LOCK**。
