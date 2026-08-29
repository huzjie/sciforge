# -*- coding: utf-8 -*-
from sciforge.schema import Hypothesis, ExperimentDesign


def test_hypothesis_defaults():
    h = Hypothesis(statement="若 X 则 Y")
    assert h.id.startswith("hyp_")
    assert h.score == 0.0


def test_experiment_design():
    d = ExperimentDesign(hypothesis_id="h1", sample_size=30)
    assert d.sample_size == 30
