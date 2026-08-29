# -*- coding: utf-8 -*-
from sciforge.providers import create
from sciforge.science.researcher import AutomatedResearcher


def test_research_runs():
    r = AutomatedResearcher(create("mock"), {"max_iterations": 3, "hypotheses_per_cycle": 2})
    report = r.research("does sleep affect memory?")
    assert report.iterations >= 1
    assert len(report.hypotheses) >= 1
    assert len(report.experiments) >= 1
    assert report.conclusion
