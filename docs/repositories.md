# 优质 GitHub 仓库介绍

> 筛选标准：近一年有维护、能直接上手、场景明确。  
> 整理时间：2026-10-18

## 快速选择

| 目标 | 先看 |
|---|---|
| 做 AI 应用 | Dify / LangGraph |
| 本地跑模型 | Ollama / vLLM |
| 做 RAG | LlamaIndex |
| 做 Agent | OpenAI Agents SDK / MCP servers |
| 做评测观测 | Langfuse / promptfoo |
| Windows 提效 | PowerToys / ShareX |
| 自托管相册 | Immich |

## 1. AI 应用与 Agent

- **[langgenius/dify](https://github.com/langgenius/dify)** — 可视化 LLM 应用平台，Docker 起服务，RAG/Agent/工作流一体。
- **[open-webui/open-webui](https://github.com/open-webui/open-webui)** — 本地/远程 LLM 的 ChatGPT 式 Web UI，支持多用户、RAG 和工具。
- **[langchain-ai/langgraph](https://github.com/langchain-ai/langgraph)** — 用图/状态机编排有状态 Agent，适合复杂分支和人工审核。
- **[openai/openai-agents-python](https://github.com/openai/openai-agents-python)** — 轻量 Agent 框架，内置 handoff、guardrails、session、tracing。
- **[modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers)** — MCP 官方参考服务器，让模型接文件、Git、数据库等工具。

## 2. 模型运行与推理

- **[ollama/ollama](https://github.com/ollama/ollama)** — 一条命令本地跑开源模型，提供 OpenAI 兼容 API。
- **[vllm-project/vllm](https://github.com/vllm-project/vllm)** — 高吞吐推理服务，支持 PagedAttention、continuous batching。
- **[sgl-project/sglang](https://github.com/sgl-project/sglang)** — 高性能 Serving 框架，适合高并发和结构化生成。
- **[huggingface/transformers](https://github.com/huggingface/transformers)** — 模型定义、推理和训练的标准库。

## 3. RAG、记忆与评测

- **[run-llama/llama_index](https://github.com/run-llama/llama_index)** — 文档解析、索引、RAG 和 Agent workflow 工具箱。
- **[mem0ai/mem0](https://github.com/mem0ai/mem0)** — 可插拔长期记忆层，适合聊天助手和个人 Agent。
- **[langfuse/langfuse](https://github.com/langfuse/langfuse)** — Trace、Eval、Prompt 管理，开源自托管。
- **[promptfoo/promptfoo](https://github.com/promptfoo/promptfoo)** — 声明式评测、红队和 CI，支持多家模型对比。
- **[BerriAI/litellm](https://github.com/BerriAI/litellm)** — 统一 100+ 模型 API，支持成本追踪、fallback、预算和代理。

## 4. 数据与云原生

- **[DataTalksClub/data-engineering-zoomcamp](https://github.com/DataTalksClub/data-engineering-zoomcamp)** — 免费 9 周数据工程训练营，含作业和项目。
- **[duckdb/duckdb](https://github.com/duckdb/duckdb)** — 嵌入式 OLAP，一条 SQL 直接查 Parquet/CSV。
- **[pola-rs/polars](https://github.com/pola-rs/polars)** — Rust 实现的 DataFrame，惰性执行、多线程。
- **[k3s-io/k3s](https://github.com/k3s-io/k3s)** — 单二进制轻量 K8s，一条命令起集群。

## 5. Web 全栈

- **[vercel/next.js](https://github.com/vercel/next.js)** — React 全栈框架，支持 App Router、SSR、Server Actions。
- **[shadcn-ui/ui](https://github.com/shadcn-ui/ui)** — 可复制进项目的 Tailwind 组件库。
- **[supabase/supabase](https://github.com/supabase/supabase)** — Postgres + Auth + Storage + Realtime + Edge Functions。
- **[pocketbase/pocketbase](https://github.com/pocketbase/pocketbase)** — 单文件后端：SQLite + Auth + Realtime + Admin UI。

## 6. 开发工具

- **[microsoft/vscode](https://github.com/microsoft/vscode)** — 代码编辑器，插件生态丰富。
- **[microsoft/terminal](https://github.com/microsoft/terminal)** — 多标签、分屏、GPU 渲染的现代终端。
- **[DevToys-app/DevToys](https://github.com/DevToys-app/DevToys)** — 开发者转换、格式化、正则、哈希工具箱。
- **[usebruno/bruno](https://github.com/usebruno/bruno)** — 离线、Git 友好的 API 客户端。

## 7. 桌面效率

- **[microsoft/PowerToys](https://github.com/microsoft/PowerToys)** — Windows 官方效率工具集，含窗口布局、批量重命名、OCR。
- **[Flow-Launcher/Flow.Launcher](https://github.com/Flow-Launcher/Flow.Launcher)** — 快速启动和文件搜索工具。
- **[ShareX/ShareX](https://github.com/ShareX/ShareX)** — 截图、录屏、OCR、上传一体化。
- **[keepassxreboot/keepassxc](https://github.com/keepassxreboot/keepassxc)** — 离线密码管理器，支持浏览器插件和 TOTP。

## 8. 自托管与媒体

- **[immich-app/immich](https://github.com/immich-app/immich)** — 自托管 Google Photos 替代，支持手机备份和相册共享。
- **[paperless-ngx/paperless-ngx](https://github.com/paperless-ngx/paperless-ngx)** — 扫描、OCR、归档和全文搜索文档。
- **[dani-garcia/vaultwarden](https://github.com/dani-garcia/vaultwarden)** — 轻量 Bitwarden 兼容密码服务器。
- **[jellyfin/jellyfin](https://github.com/jellyfin/jellyfin)** — 自托管媒体服务器，管理电影、剧集和音乐。

## 9. 学习与 CS

- **[krahets/hello-algo](https://github.com/krahets/hello-algo)** — 动画图解数据结构与算法，多语言代码。
- **[codecrafters-io/build-your-own-x](https://github.com/codecrafters-io/build-your-own-x)** — 用任意语言重造 Redis、Git、Docker 等项目。
- **[nand2tetris/projects](https://github.com/nand2tetris/projects)** — 从 NAND 门造到 CPU/OS 的官方项目。
- **[donnemartin/system-design-primer](https://github.com/donnemartin/system-design-primer)** — 大规模系统设计入门与面试资料。

---

**建议：** 先挑 3–5 个真正用得上的，跑通 quickstart 再换下一个；商用前查看 LICENSE。
