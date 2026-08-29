# -*- coding: utf-8 -*-
"""实验设计 + mock 执行示例。"""
from sciforge.providers import create
from sciforge.schema import Hypothesis
from sciforge.science.experiment import ExperimentDesigner
from sciforge.science.lab import LabExecutor

if __name__ == "__main__":
    designer = ExperimentDesigner(create("mock"))
    h = Hypothesis(statement="咖啡因提升警觉性")
    design = designer.design(h)
    result = LabExecutor().run(design)
    print("effect_size =", result.metrics["effect_size"])
    print("conclusion =", result.conclusion)
