# sciforge

> **AI 科研智能体与自动化科学发现平台**（AI Scientific Discovery & Automated Research Platform）

**sciforge** 把当下最热的「AI 科学家」范式落地成一个可以直接部署、可以复现、可以审计的完整工程。你给它一个研究问题，它自动跑完整条科研流水线：

> **假设生成 → 假设排序 → 文献综述 → 实验设计 → 实验执行 → 统计分析 → 同行评审 → 假设精炼**，循环迭代直到收敛。

一句话：**不是"对话助手"，而是一支可以 7×24 运转的科研团队。**

---

## 一、为什么要做这个

2026 年 8 月底，AI 科研智能体集中爆发，几件事几乎是同时发生的：

| 事件 | 要点 | sciforge 对应能力 |
| --- | --- | --- |
| Google **Gemini Co-Scientist** | 自动生成假设、设计实验，发现的医疗架构超越多款前沿模型 | 假设引擎 + 研究员闭环 |
| Anthropic **自动化对齐研究员** | 研究成本从 $150/时降到 $4/时，10 项基准平均 6 小时超人类基线 | 迭代研究员 + 基准评测 |
| OpenAI **Rosalind Workbench** | 蛋白质 / 测序流水线，给每个科学家一支"可审查的研究团队" | 多智能体角色 + 溯源 |
| 斯坦福 **Terminal-Bench-Science 0.1** | 评测科研工作流里的 AI 智能体 | 基准评测套件 |
| 社区 **scientific-agent-skills** | 17.5 万科学家在用的 Agent Skills | 可复现、可插拔设计 |

这些信号指向同一个结论：**科研的瓶颈正在从"人不够聪明"变成"人不够多、不够快"**。sciforge 就是把这个结论工程化的产物——把"自动化科研"做成一个真正能跑、能审计、能复现的开源平台。

---

## 二、核心能力

### 🧪 假设引擎（Hypothesis Engine）
- 从研究问题生成**可证伪、可检验**的假设（「若 X 则 Y，机制 M，依据文献 L」句式）
- 按**可检验性 + 新颖性**打分排序，自动聚焦最值得验证的假设

### 🔁 自动化研究员（Automated Researcher）
- 对标 Anthropic「自动化对齐研究员」的**迭代闭环**：假设 → 排序 → 文献 → 实验 → 分析 → 精炼
- 支持最大迭代轮数、收敛阈值、自动精炼开关，全部可配置

### ⚗️ 实验设计与执行（Experiment Design & Lab）
- 从假设自动推导**独立变量 / 因变量 / 控制变量 / 方法 / 样本量**
- 内置**确定性 mock 实验室**（离线可演示），并预留真实硬件 / 湿实验适配器接口

### 📈 统计分析（Statistics）
- 均值 / 方差 / **Cohen's d 效应量** / **近似 Welch t 检验**（纯标准库 `math.erf` 实现）

### 🧾 可复现溯源（Provenance）
- 每个产物记录 **SHA-256 哈希 + 血缘链**，支持从任意节点回溯完整推导过程

### 🏆 基准评测（Benchmark）
- 内置 **hypothesis / literature / experiment / reasoning** 四套件，对标 Terminal-Bench-Science

### 🤝 多智能体角色（Agent Roles）
- 科学家 / 审稿人 / 统计学家 / 文献员 / 实验员，各自绑定独立 system prompt 与生命周期状态机

### 📡 9 家 LLM Provider
- OpenAI / Anthropic / Gemini / DeepSeek / Qwen / Kimi / GLM / Ollama / **Mock**（完全离线）
- 核心 HTTP 调用用**标准库 urllib** 实现，**零第三方依赖**

### 🖥️ 双控制面 + SDK + 控制台
- **FastAPI** 控制面（装了就能用）+ **纯标准库 HTTP 服务**兜底
- **CLI**（`doctor` / `hypothesize` / `search` / `design` / `run` / `benchmark` / `serve`）
- **Python SDK** + **TypeScript SDK**
- **React 深色控制台**（Vite）

### 🔐 安全与可观测
- **拒绝式默认**安全策略引擎（按规则顺序首个匹配）
- **JSONL 追加式审计日志**、**Prometheus 指标**、**W3C traceparent 追踪**

### 📦 完整工程化
- Docker / docker-compose / K8s / Helm / GitHub Actions CI / CodeQL / dependabot

---

## 三、快速开始

```bash
git clone https://github.com/huzjie/sciforge.git
cd sciforge

# 1. 自检（离线可用，会列出 9 家 Provider 状态）
python -m sciforge doctor

# 2. 跑一次完整科研闭环
python -m sciforge run "睡眠不足是否影响记忆巩固？"

# 3. 单独生成假设
python -m sciforge hypothesize "某药物是否通过抑制炎症通路缓解症状？" -n 3

# 4. 文献检索
python -m sciforge search "深度学习 蛋白质结构预测"

# 5. 实验设计
python -m sciforge design "咖啡因提升警觉性"

# 6. 基准评测
python -m sciforge benchmark

# 7. 启动控制面
python -m sciforge serve --host 0.0.0.0 --port 8000
```

启动控制面后访问 `http://localhost:8000/docs`（FastAPI）或直接调用：

```bash
curl http://localhost:8000/healthz
curl -X POST http://localhost:8000/research -H "Content-Type: application/json" \
     -d '{"question": "运动是否改善认知功能？"}'
```

---

## 四、配置

复制 `config.example.json` 为 `config.json`，或用环境变量覆盖（双下划线表层级）：

```bash
# 切换 Provider
export SCIFORGE_PROVIDER=deepseek

# 给某个 Provider 配置密钥 / 模型
export SCIFORGE_PROVIDERS__DEEPSEEK__API_KEY=sk-xxxx
export SCIFORGE_PROVIDERS__DEEPSEEK__MODEL=deepseek-chat

# 调研究员参数
export SCIFORGE_RESEARCHER__MAX_ITERATIONS=50
```

---

## 五、架构

```
sciforge/
├── science/           # 核心科研领域：假设/文献/实验/实验室/研究员/基准/溯源/统计/评审
├── agents/            # 多智能体角色 + 生命周期状态机
├── providers/         # 9 家 LLM Provider（mock 可离线）
├── storage/           # SQLite + 内存存储
├── security/          # 拒绝式默认策略引擎 + 审计日志
├── observability/     # Prometheus 指标 + W3C 追踪
├── api/               # FastAPI + 纯标准库控制面
├── cli.py             # 命令行
├── sdk.py             # Python SDK
└── orchestrator.py    # 统一装配点
web/                   # React 深色控制台
sdk/                   # TypeScript SDK
deploy/                # K8s + Helm
docs/                  # 12 篇文档
examples/              # 8 个可运行示例
tests/                 # 单元测试
```

---

## 六、扩展点

- **接入真实实验室**：实现 `LabExecutor` 的适配器（机械臂 / 湿实验 / 仿真）
- **接入文献库**：替换 `LiteratureSearch.search` 的离线兜底，对接 PubMed / Semantic Scholar / arXiv
- **自定义角色**：在 `agents/roles.py` 注册新科研角色
- **自定义基准**：向 `ScienceBenchmark` 注册新评测套件

---

## 七、许可证

Apache-2.0。详见 [LICENSE](LICENSE)。
