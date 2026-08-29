# -*- coding: utf-8 -*-
from sciforge.schema import ExperimentDesign
from sciforge.science.lab import LabExecutor


def test_deterministic():
    lab = LabExecutor()
    d = ExperimentDesign(hypothesis_id="h1", sample_size=30)
    r1 = lab.run(d)
    r2 = lab.run(d)
    assert r1.metrics["effect_size"] == r2.metrics["effect_size"]


def test_effect_in_range():
    lab = LabExecutor()
    d = ExperimentDesign(hypothesis_id="h1", sample_size=30)
    r = lab.run(d)
    assert 0.0 <= r.metrics["effect_size"] <= 1.0
