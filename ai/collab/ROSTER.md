# 四人编组与代号

| 代号 | Agent | 角色 | 一句话 |
|---|---|---|---|
| **CUR** | Cursor | **总调度 + 主改稿** | 派单、占锁、改 `papers.md` / 时间线；汇总 logs，触发验证 |
| **CDX** | Codex | **工程 + 扩写主笔（P1-a）** | 脚本/测试/JS；**batch 扩写 JSON**（派单后）；不 merge `papers.md` |
| **DSH** | DeepSeek Harness | **验证** | 只读 + `mkdocs build --strict` + 数据校验报告 |
| **WKB** | WorkBuddy | **内容备援 / 元数据** | P1-c 占位清理、批量脚本（CUR 派单）；非默认扩写主责 |

**用户**：批准派单、在四个客户端之间转发一句「看 `DISPATCH.md`」。

---

## 总调度（CUR）专有职责

1. 维护 **`DISPATCH.md`**（当前谁干什么、阻塞项、下一步）。
2. 维护 **`PLAN.md`** 任务状态（待办 → 进行中 → 待验证 → 完成）。
3. **独占决策** `docs/papers.md` 的写入时机（更新 `LOCK.md`）。
4. 阅读全员 `logs/`，合并冲突指令，写 **`logs/*-cursor-dispatch-*.md`**。
5. 改完一批功能后，在日志写 **「请 DSH 验证」**；DSH 通过后写 **「请用户验收」**。

其他三人 **不互相派单**，只认 `DISPATCH.md` + `LOCK.md`。

---

## 文件 ownership（默认）

| 路径 | 主责 | 备援（须 CUR 派单） |
|---|---|---|
| `docs/papers.md` | **CUR** | 无（禁止 CDX/WKB/DSH 写） |
| `docs/ai-timeline.md` | **CUR** | CDX 可改链接（派单 P0-2） |
| `docs/javascripts/papers-shelf.js` | **CUR** | **CDX**（派单 P0-3） |
| `docs/stylesheets/papers-workbench.css` | **CUR** | CDX |
| `scripts/*.py`（内容流水线） | **CDX**（P1-a 扩写 batch） | **WKB**（P1-c 等，CUR 派单） |
| `ai/collab/*` | **CUR** | 全员只读；各角色只写自己的 `logs/` 与 `outbox/` |
| 构建产物 / `.venv` | **DSH** 只读执行 | — |

---

## 通信规则

```text
CUR 更新 DISPATCH.md
    ↓
用户转发：「你是 <代号>，读 ai/collab/DISPATCH.md 执行你的行」
    ↓
CDX / DSH / WKB 写 logs/，更新 outbox/<角色>/latest.md
    ↓
CUR 读 logs，更新 DISPATCH + PLAN，再派下一棒
```

禁止：CDX 与 WKB 同时持锁；任何人未读 LOCK 就改 `papers.md`。
