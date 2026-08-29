# -*- coding: utf-8 -*-
"""实验设计：从假设推导实验方案并做完整性校验。"""
from __future__ import annotations

from ..providers.base import BaseProvider
from ..schema import ExperimentDesign, ExperimentStatus, Hypothesis


class ExperimentDesigner:
    def __init__(self, provider: BaseProvider):
        self.provider = provider

    def design(self, hypothesis: Hypothesis) -> ExperimentDesign:
        prompt = "请为如下假设设计实验（给出独立变量、因变量、控制变量、方法、样本量）：\n%s" % hypothesis.statement
        text = self.provider.complete(prompt)
        d = ExperimentDesign(
            hypothesis_id=hypothesis.id,
            independent_vars=_pick(text, "独立变量", ["处理组"]),
            dependent_vars=_pick(text, "因变量", ["结果指标"]),
            controls=_pick(text, "控制变量", ["基线", "环境"]),
            method="随机对照试验",
            protocol=text,
            sample_size=_parse_int(text, 30),
            status=ExperimentStatus.DESIGNED.value,
        )
        return d

    def validate(self, design: ExperimentDesign) -> bool:
        return bool(design.independent_vars and design.dependent_vars)


def _pick(text: str, keyword: str, default: list) -> list:
    for line in text.splitlines():
        if keyword in line:
            parts = line.replace(keyword, "").strip(" :：")
            items = [p.strip() for p in parts.replace("、", ",").split(",") if p.strip()]
            if items:
                return items
    return default


def _parse_int(text: str, default: int) -> int:
    for word in text.replace("：", " ").replace(":", " ").split():
        if word.isdigit():
            return int(word)
    return default


__all__ = ["ExperimentDesigner"]
