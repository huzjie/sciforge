# -*- coding: utf-8 -*-
"""接入真实 Provider 示例（需配置 API Key）。"""
import os
from sciforge.orchestrator import ResearchOrchestrator

if __name__ == "__main__":
    os.environ["SCIFORGE_PROVIDER"] = "deepseek"
    os.environ["SCIFORGE_PROVIDERS__DEEPSEEK__API_KEY"] = "sk-xxxx"
    orch = ResearchOrchestrator()
    report = orch.run("你的研究问题")
    print(report.conclusion)
