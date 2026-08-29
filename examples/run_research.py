# -*- coding: utf-8 -*-
"""端到端科研闭环示例。"""
from sciforge.orchestrator import ResearchOrchestrator

if __name__ == "__main__":
    orch = ResearchOrchestrator()
    report = orch.run("睡眠不足是否影响记忆巩固？")
    print(report.conclusion)
    for h in report.hypotheses[:3]:
        print("[%.3f] %s" % (h.score, h.statement))
