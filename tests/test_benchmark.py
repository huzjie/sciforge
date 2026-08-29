# -*- coding: utf-8 -*-
from sciforge.providers import create
from sciforge.science.benchmark import ScienceBenchmark


def test_cases():
    b = ScienceBenchmark(create("mock"))
    assert len(b.cases()) >= 4


def test_run_scores():
    b = ScienceBenchmark(create("mock"))
    results = b.run()
    assert len(results) == len(b.cases())
    assert all(0.0 <= r.score <= 1.0 for r in results)
