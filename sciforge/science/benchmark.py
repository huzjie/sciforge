# -*- coding: utf-8 -*-
"""科研工作流基准评测（对标 Terminal-Bench-Science 思路）。"""
from __future__ import annotations

import difflib
from typing import List

from ..providers.base import BaseProvider
from ..schema import BenchmarkCase, BenchmarkResult

_BUILTIN_CASES = [
    BenchmarkCase(name="hypothesis_basic", suite="hypothesis",
                  prompt="研究问题：睡眠不足是否影响记忆巩固？提出一个可检验假设。",
                  reference="机制"),
    BenchmarkCase(name="hypothesis_advanced", suite="hypothesis",
                  prompt="研究问题：某药物是否通过抑制炎症通路缓解症状？提出机制性假设。",
                  reference="通路"),
    BenchmarkCase(name="literature_synthesis", suite="literature",
                  prompt="请综合评述「深度学习用于蛋白质结构预测」的进展。",
                  reference="综合"),
    BenchmarkCase(name="experiment_design", suite="experiment",
                  prompt="为「咖啡因提升警觉性」设计一个含对照组的实验。",
                  reference="对照"),
    BenchmarkCase(name="reasoning_causal", suite="reasoning",
                  prompt="解释相关性与因果性的区别，并给出识别因果的方法。",
                  reference="因果"),
]


class ScienceBenchmark:
    def __init__(self, provider: BaseProvider):
        self.provider = provider

    def cases(self, suite: str = "") -> List[BenchmarkCase]:
        if not suite:
            return list(_BUILTIN_CASES)
        return [c for c in _BUILTIN_CASES if c.suite == suite]

    def run(self, suite: str = "") -> List[BenchmarkResult]:
        results = []
        for case in self.cases(suite):
            output = self.provider.complete(case.prompt)
            score = self._rubric(case, output)
            results.append(BenchmarkResult(
                case_id=case.id, output=output, score=score,
                metrics={"rubric": score},
            ))
        return results

    def _rubric(self, case: BenchmarkCase, output: str) -> float:
        # 关键词重合度评分（简化的 rubric）
        ref_words = [w for w in case.reference.replace("，", " ").split() if len(w) >= 2]
        if not ref_words:
            return 1.0 if output.strip() else 0.0
        hit = sum(1 for w in ref_words if w in output)
        base = hit / len(ref_words)
        if base > 0:
            base += 0.1 * min(1.0, len(output) / 200.0)
        return round(min(1.0, base), 4)


__all__ = ["ScienceBenchmark"]
