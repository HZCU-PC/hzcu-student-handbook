# P1 冲刺 PLAN

> 状态与派单见 `DISPATCH.md`。基准审计：`python scripts/p1_audit.py`

## 目标

降低论文页「模板感」与数据不一致；不破坏 205 条 JSON ↔ 卡片 id 对齐。

## 任务

| ID | 任务 | 负责人 | 验收 | 状态 |
|---|---|---|---|---|
| P1-js | 旧深链映射 | **CUR** | `?id=B01` → 反向传播 | 完成 |
| P1-cit / P1-d / P1-gen | 角标、expand、regenerate | **CDX**+**CUR** | V-3 通过 | 完成 |
| **P1-a** | 扩写 | **CDX**（主） | template 下降 | batch05 CUR ✓ · **batch06 CDX 进行中** |
| **P1-c** | 占位 authors / arXiv link | **WKB**（备援） | 92→下降 | 待派 |
| V-3 | gen 合并 | **DSH** | 通过 | 完成 |

## 内容阶段

1. CDX/WKB 产出 batch（JSON patch）— 写作见 **`P1-VOICE.md`**
2. CUR merge + regenerate + audit

## 批次建议

- 每批 ≤20 篇；log 列 id 与事实核对即可，**不附 mandatory 句式模板**

## P0 关单

用户已下令 **P1** → P0 视为验收通过（功能修复已交付）。
