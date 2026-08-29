# sciforge

> AI 科研智能体与自动化科学发现平台 — AI Scientific Discovery & Automated Research Platform

**sciforge** 把「AI 科学家」落地为可部署、可复现、可审计的完整平台：从研究问题出发，自动完成**假设生成 → 假设排序 → 文献综述 → 实验设计 → 实验执行 → 统计分析 → 同行评审 → 假设精炼**的完整科研闭环。内核**纯 Python 标准库零第三方运行时依赖**，`mock` 模式完全离线可跑。

## ✨ 能力一览

- 🧪 **假设引擎**：从研究问题生成可证伪假设，并按可检验性/新颖性打分排序
- 📚 **文献检索与综述**：检索相关文献、生成结构化综述
- ⚗️ **实验设计与执行**：自动推导独立/因变量、控制变量与方法；mock 实验室确定性产出
- 🔁 **自动化研究员**：30 分钟迭代闭环（对标 Anthropic 自动化对齐研究员），自动收敛
- 📈 **统计分析**：均值/方差/Cohen's d/近似 Welch t 检验（纯标准库）
- 🧾 **可复现溯源**：每个产物记录 SHA-256 哈希与血缘链，支持重放
- 🏆 **基准评测**：内置 hypothesis/literature/experiment/reasoning 四套件（对标 Terminal-Bench-Science）
- 🤝 **多智能体角色**：科学家/审稿人/统计学家/文献员/实验员
- 📡 **9 家 LLM Provider**：OpenAI/Anthropic/Gemini/DeepSeek/Qwen/Kimi/GLM/Ollama/Mock
- 🖥️ **双控制面**：FastAPI + 纯标准库 HTTP 服务、CLI、Python/TS SDK、React 深色控制台
- 🔐 **安全与可观测**：拒绝式默认策略引擎、JSONL 审计日志、Prometheus 指标、W3C 追踪
- 📦 **完整工程化**：Docker/K8s/Helm/CI/CodeQL

## 🚀 快速开始

```bash
git clone https://github.com/huzjie/sciforge.git
cd sciforge
python -m sciforge doctor            # 自检（离线可用，9 Provider）
python -m sciforge run "睡眠不足是否影响记忆巩固？"   # 完整科研闭环
python -m sciforge hypothesize "某药物是否通过抑制炎症通路缓解症状？"
python -m sciforge benchmark         # 基准评测
python -m sciforge serve --port 8000 # 控制面
```

## 🧩 配置

复制 `config.example.json` 为 `config.json`，或通过环境变量覆盖（`__` 表层级）：

```bash
export SCIFORGE_PROVIDER=deepseek
export SCIFORGE_PROVIDERS__DEEPSEEK__API_KEY=sk-...
```

## 📖 文档

见 [`docs/`](docs/) 目录：快速上手、架构、概念、Provider、假设引擎、研究员闭环、基准、溯源、部署、API、安全、FAQ。

## 🧱 架构

```
sciforge/
├── science/        # 假设/文献/实验/实验室/研究员/基准/溯源/统计/评审
├── agents/         # 多智能体角色与生命周期
├── providers/      # 9 家 LLM Provider（mock 可离线）
├── storage/        # SQLite + 内存存储
├── security/       # 策略引擎 + 审计
├── observability/  # Prometheus 指标 + W3C 追踪
├── api/            # FastAPI + 纯标准库控制面
├── cli.py / sdk.py # CLI 与 Python SDK
└── orchestrator.py # 统一装配
```

## 许可证

Apache-2.0。详见 [LICENSE](LICENSE)。
