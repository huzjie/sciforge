# 架构

sciforge 采用分层架构：

- **领域层**（science）：假设/文献/实验/研究员等核心科研能力
- **智能体层**（agents）：多角色与生命周期
- **适配层**（providers）：9 家 LLM，mock 可离线
- **平台层**（api/cli/sdk）：对外控制面
- **横切层**（security/observability/storage）

统一装配点：`sciforge/orchestrator.py`。
