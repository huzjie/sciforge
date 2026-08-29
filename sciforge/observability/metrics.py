# -*- coding: utf-8 -*-
"""Prometheus 文本格式指标（零依赖）。"""
from __future__ import annotations

import time
from typing import Dict, List


class MetricsRegistry:
    def __init__(self) -> None:
        self._counters: Dict[str, float] = {}
        self._gauges: Dict[str, float] = {}
        self._started = time.time()

    def inc(self, name: str, value: float = 1.0) -> None:
        self._counters[name] = self._counters.get(name, 0.0) + value

    def set(self, name: str, value: float) -> None:
        self._gauges[name] = value

    def render(self) -> str:
        lines: List[str] = []
        for k, v in sorted(self._counters.items()):
            lines.append("# TYPE %s counter" % k)
            lines.append("%s %s" % (k, _fmt(v)))
        for k, v in sorted(self._gauges.items()):
            lines.append("# TYPE %s gauge" % k)
            lines.append("%s %s" % (k, _fmt(v)))
        lines.append("sciforge_uptime_seconds %s" % _fmt(time.time() - self._started))
        return "\n".join(lines) + "\n"


def _fmt(v: float) -> str:
    return ("%f" % v).rstrip("0").rstrip(".")


__all__ = ["MetricsRegistry"]
