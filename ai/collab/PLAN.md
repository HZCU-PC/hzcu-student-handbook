# 当前冲刺 PLAN

> 任务内容见本文件；**负责人与状态以 `DISPATCH.md` 为准**。总调度 **CUR** 更新状态。

## 状态

- **冲刺名：** 论文浏览页 P0 功能修复
- **状态：** P0 已完成；**P1 进行中**（见 `PLAN-P1.md`）
- **最后更新：** 2026-11-03 23:50

## 目标

修复论文浏览页三个 P0，使筛选、空状态、深链、时间线跳转、JS 不重复执行。

## 任务列表

| 序号 | 任务 | 负责人 | 验收标准 | 状态 |
|---|---|---|---|---|
| P0-1 | 在 `docs/papers.md` 最后一个 `</article>` 与 `#empty` 之间补 `</div>` 关闭 `.paper-grid` | **CUR** | 筛选后 `#empty` 仍存在于 DOM；无 `getElementById('empty')` 报错 | 完成 |
| P0-2 | 更新 `docs/ai-timeline.md` 11 处深链为正确 `?id=WB-*`（见 PROJECT-CONTEXT 映射表） | **CUR** | 从时间线点进对应论文介绍弹窗 | 完成 |
| P0-3 | 删除 `papers.md` 内联 script；仅保留 `papers-shelf.js`；加 null 守卫与深链 id 解析 | **CUR** | 论文页 init 只跑一次；非论文页无 JS 报错 | 完成 |
| V-1 | `mkdocs build --strict` + 数据一致性抽查 | **DSH** | 构建零警告；205 卡片与 JSON 一致 | **完成** |

## 完成后

1. ~~Cursor 写 `logs/*-cursor-p0-done.md`~~ ✓  
2. ~~DSH 写 `logs/*-dsh-verify-p0.md`~~ ✓（`2026-11-03-2344-dsh-verify-p0.md`）  
3. **用户**浏览器点检 4 项 → 对 CUR 确认 → 可标记冲刺 **P0 已完成** 并启动 P1。
