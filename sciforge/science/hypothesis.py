# -*- coding: utf-8 -*-
"""假设引擎：从研究问题生成候选假设并排序。"""
from __future__ import annotations

from typing import List

from ..providers.base import BaseProvider
from ..schema import Hypothesis, HypothesisStatus

_SYSTEM = ("你是一位严谨的科研人员。基于研究问题，提出可证伪、可检验的科学假设，"
           "并用「若 X 则 Y，机制 M，依据文献 L」的句式表达。")


class HypothesisEngine:
    def __init__(self, provider: BaseProvider):
        self.provider = provider

    def generate(self, question: str, n: int = 3) -> List[Hypothesis]:
        prompt = (
            "研究问题：%s\n\n请提出 %d 个可检验的科学假设（hypothesis），"
            "每个假设用一句话，包含机制与预测。" % (question, n)
        )
        text = self.provider.chat([
            {"role": "system", "content": _SYSTEM},
            {"role": "user", "content": prompt},
        ])
        statements = _split_statements(text, n)
        hyps = [Hypothesis(statement=s) for s in statements]
        return hyps

    def rank(self, hypotheses: List[Hypothesis], question: str = "") -> List[Hypothesis]:
        ranked = []
        for h in hypotheses:
            score = self._score(h.statement, question)
            h.score = score
            h.status = HypothesisStatus.RANKED.value
            ranked.append(h)
        ranked.sort(key=lambda x: x.score, reverse=True)
        return ranked

    def _score(self, statement: str, question: str) -> float:
        prompt = "请对该假设的可检验性与新颖性打分（0 到 1 的单一小数）：%s" % statement
        text = self.provider.complete(prompt)
        return _parse_score(text)


def _split_statements(text: str, n: int) -> List[str]:
    raw = [s.strip(" -\n\t0123456789.") for s in text.splitlines() if s.strip()]
    raw = [s for s in raw if len(s) > 5]
    if not raw:
        raw = [text.strip()]
    return raw[:n]


def _parse_score(text: str) -> float:
    try:
        val = float(text.strip())
        return max(0.0, min(1.0, val))
    except ValueError:
        return 0.5


__all__ = ["HypothesisEngine"]
