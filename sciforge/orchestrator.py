# -*- coding: utf-8 -*-
"""研究编排器：统一装配 Provider / 安全策略 / 观测 / 审计 / 存储。"""
from __future__ import annotations

from typing import Any, Dict, List, Optional

from .config import load_config
from .errors import SecurityError
from .observability.metrics import MetricsRegistry
from .observability.trace import TraceContext
from .providers import create
from .schema import Hypothesis, ExperimentResult
from .science.benchmark import ScienceBenchmark
from .science.researcher import AutomatedResearcher, ResearchReport
from .security.audit import AuditLog
from .security.policy import PolicyEngine


class ResearchOrchestrator:
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or load_config()
        self.provider = create(
            self.config["provider"],
            self.config.get("providers", {}).get(self.config["provider"], {}),
        )
        self.policy = PolicyEngine()
        self.metrics = MetricsRegistry()
        self.audit = AuditLog(self.config.get("storage", {}).get("audit", "./data/audit.jsonl"))
        self.researcher = AutomatedResearcher(self.provider, self.config.get("researcher", {}))
        self.benchmark = ScienceBenchmark(self.provider)

    def run(self, question: str) -> ResearchReport:
        self.policy.guard("run")
        self.metrics.inc("sciforge_research_runs")
        self.audit.record("run", meta={"question": question})
        report = self.researcher.research(question)
        self.metrics.inc("sciforge_hypotheses_total", len(report.hypotheses))
        self.metrics.inc("sciforge_experiments_total", len(report.experiments))
        return report

    def doctor(self) -> Dict[str, Any]:
        return {
            "provider": self.provider.name,
            "provider_ok": self.provider.healthcheck(),
            "providers_available": list(sorted(self.provider_health())),
            "max_iterations": self.researcher.max_iterations,
        }

    def provider_health(self) -> Dict[str, bool]:
        from .providers import REGISTRY, create as _create
        out = {}
        for name, cls in REGISTRY.items():
            try:
                out[name] = _create(name, self.config.get("providers", {}).get(name, {})).healthcheck()
            except Exception:
                out[name] = False
        return out


__all__ = ["ResearchOrchestrator"]
