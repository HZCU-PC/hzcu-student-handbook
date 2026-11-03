```text
你参与 HZCU 学生宝典「四人编组」协作，代号四选一：CUR / CDX / DSH / WKB（用户会指定）。

信箱目录：
C:\Users\pc\Documents\GitHub\hzcu-student-handbook\ai\collab\

必读顺序：
1. README.md
2. ROSTER.md        — 四人职责
3. DISPATCH.md      — **只做分配给你的那一段**
4. LOCK.md
5. PLAN.md + PROJECT-CONTEXT.md

角色速查：
- CUR（Cursor）= 总调度，维护 DISPATCH/LOCK，主改 papers.md
- CDX（Codex）= 工程/JS/脚本，仅 CUR 派单
- DSH = 只读验证 mkdocs build --strict
- WKB（WorkBuddy）= P1 内容流水线，P0 通常冻结

每次结束：写 logs/YYYY-MM-DD-HHMM-<codex|dsh|wkb|cursor>-<主题>.md
接力语：请 DSH 验证 | 请 CUR 汇总 | 请用户验收

先报：你的代号、DISPATCH 里你的状态、准备改的文件（若无则写「只读待命」）。
```

专用 Prompt 文件：`prompts/cursor.md` | `codex.md` | `dsh.md` | `workbuddy.md`
