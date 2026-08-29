# -*- coding: utf-8 -*-
"""统计分析：均值/方差/效应量/近似 t 检验（纯标准库）。"""
from __future__ import annotations

import math
from typing import List, Tuple


class StatisticalAnalyzer:
    @staticmethod
    def mean(values: List[float]) -> float:
        return sum(values) / len(values) if values else 0.0

    @staticmethod
    def std(values: List[float], ddof: int = 1) -> float:
        if len(values) < 2:
            return 0.0
        m = StatisticalAnalyzer.mean(values)
        var = sum((x - m) ** 2 for x in values) / (len(values) - ddof)
        return math.sqrt(var)

    @classmethod
    def cohens_d(cls, group_a: List[float], group_b: List[float]) -> float:
        na, nb = len(group_a), len(group_b)
        if na < 2 or nb < 2:
            return 0.0
        sa, sb = cls.std(group_a), cls.std(group_b)
        pooled = math.sqrt(((na - 1) * sa ** 2 + (nb - 1) * sb ** 2) / (na + nb - 2))
        if pooled == 0:
            return 0.0
        return (cls.mean(group_a) - cls.mean(group_b)) / pooled

    @classmethod
    def welch_t(cls, group_a: List[float], group_b: List[float]) -> Tuple[float, float]:
        """返回 (t 统计量, 双侧近似 p 值)。"""
        na, nb = len(group_a), len(group_b)
        if na < 2 or nb < 2:
            return 0.0, 1.0
        ma, mb = cls.mean(group_a), cls.mean(group_b)
        va, vb = cls.var(group_a), cls.var(group_b)
        se = math.sqrt(va / na + vb / nb)
        if se == 0:
            return 0.0, 1.0
        t = (ma - mb) / se
        p = cls._approx_p(t)
        return t, p

    @staticmethod
    def var(values: List[float]) -> float:
        return StatisticalAnalyzer.std(values) ** 2

    @staticmethod
    def _approx_p(t: float) -> float:
        # 正态近似（大样本），math.erf 计算双尾 p
        z = abs(t)
        p = math.erfc(z / math.sqrt(2.0))
        return max(0.0, min(1.0, p))


__all__ = ["StatisticalAnalyzer"]
