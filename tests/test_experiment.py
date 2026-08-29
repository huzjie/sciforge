# -*- coding: utf-8 -*-
from sciforge.providers import create
from sciforge.schema import Hypothesis
from sciforge.science.experiment import ExperimentDesigner


def test_design():
    d = ExperimentDesigner(create("mock"))
    design = d.design(Hypothesis(statement="test"))
    assert design.hypothesis_id
    assert d.validate(design)
