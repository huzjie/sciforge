# -*- coding: utf-8 -*-
"""实验执行器：mock 模式确定性产出，可对接真实实验室适配器。"""
from __future__ import annotations

import hashlib
import json
from typing import Dict

from ..schema import ExperimentDesign, ExperimentResult


class LabExecutor:
    """实验执行器。默认 mock（确定性），可扩展真实硬件/湿实验适配器。"""

    def __init__(self, mode: str = "mock"):
        self.mode = mode

    def run(self, design: ExperimentDesign, seed: str = "") -> ExperimentResult:
        if self.mode == "mock":
            return self._run_mock(design, seed)
        raise NotImplementedError("仅支持 mock 模式，真实适配器请实现 LabAdapter")

    def _run_mock(self, design: ExperimentDesign, seed: str) -> ExperimentResult:
        key = json.dumps({
            "h": design.hypothesis_id,
            "iv": design.independent_vars,
            "dv": design.dependent_vars,
            "seed": seed,
        }, sort_keys=True).encode("utf-8")
        digest = hashlib.sha256(key).hexdigest()
        effect = (int(digest[:8], 16) % 1000) / 1000.0  # 0..1
        n = design.sample_size or 30
        observations = {
            "treatment_mean": round(0.50 + effect, 4),
            "control_mean": round(0.50, 4),
            "n": n,
            "std": round(0.10, 4),
        }
        metrics = {
            "effect_size": round(effect, 4),
            "cohens_d": round(effect / 0.10, 4),
        }
        conclusion = "效应量 %.3f（%s）" % (effect, "显著" if effect > 0.2 else "不显著")
        return ExperimentResult(
            design_id=design.id,
            observations=observations,
            metrics=metrics,
            conclusion=conclusion,
        )


__all__ = ["LabExecutor"]
