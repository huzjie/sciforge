# -*- coding: utf-8 -*-
"""自动化研究员：假设 -> 排序 -> 文献 -> 实验 -> 分析 -> 精炼 的迭代闭环。"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import List

from ..providers.base import BaseProvider
from ..schema import Hypothesis, ExperimentResult, HypothesisStatus
from .hypothesis import HypothesisEngine
from .literature import LiteratureSearch
from .experiment import ExperimentDesigner
from .lab import LabExecutor
from .review import PeerReviewer


@dataclass
class ResearchReport:
    question: str
    iterations: int = 0
    hypotheses: List[Hypothesis] = field(default_factory=list)
    experiments: List[ExperimentResult] = field(default_factory=list)
    conclusion: str = ""
    converged: bool = False

    def to_dict(self) -> dict:
        return {
            "question": self.question,
            "iterations": self.iterations,
            "hypotheses": [h.to_dict() for h in self.hypotheses],
            "experiments": [e.to_dict() for e in self.experiments],
            "conclusion": self.conclusion,
            "converged": self.converged,
        }


class AutomatedResearcher:
    def __init__(self, provider: BaseProvider, config: dict | None = None):
        cfg = config or {}
        self.provider = provider
        self.max_iterations = int(cfg.get("max_iterations", 30))
        self.hypotheses_per_cycle = int(cfg.get("hypotheses_per_cycle", 3))
        self.threshold = float(cfg.get("convergence_threshold", 0.02))
        self.engine = HypothesisEngine(provider)
        self.literature = LiteratureSearch(provider)
        self.designer = ExperimentDesigner(provider)
        self.lab = LabExecutor()
        self.reviewer = PeerReviewer(provider)

    def research(self, question: str) -> ResearchReport:
        report = ResearchReport(question=question)
        best_score = 0.0

        for i in range(self.max_iterations):
            hyps = self.engine.generate(question, self.hypotheses_per_cycle)
            ranked = self.engine.rank(hyps, question)
            if not ranked:
                break
            top = ranked[0]
            if top.statement not in {h.statement for h in report.hypotheses}:
                report.hypotheses.append(top)

            design = self.designer.design(top)
            result = self.lab.run(design, seed=question + str(i))
            report.experiments.append(result)

            delta = abs(top.score - best_score)
            best_score = max(best_score, top.score)

            report.iterations = i + 1
            if top.score >= 0.9 or (i > 2 and delta < self.threshold):
                report.converged = True
                top.status = HypothesisStatus.CONFIRMED.value
                break

        report.conclusion = self._conclude(report)
        return report

    def _conclude(self, report: ResearchReport) -> str:
        if not report.experiments:
            return "未产生实验。"
        effects = [e.metrics.get("effect_size", 0.0) for e in report.experiments]
        avg = sum(effects) / len(effects)
        return ("共 %d 轮迭代、%d 条假设、%d 次实验；平均效应量 %.3f；%s收敛。" %
                (report.iterations, len(report.hypotheses), len(report.experiments),
                 avg, "已" if report.converged else "未"))


__all__ = ["AutomatedResearcher", "ResearchReport"]
