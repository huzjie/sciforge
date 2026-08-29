# -*- coding: utf-8 -*-
from sciforge.providers import create
from sciforge.science.hypothesis import HypothesisEngine


def test_generate():
    e = HypothesisEngine(create("mock"))
    hyps = e.generate("does X cause Y?", n=2)
    assert len(hyps) >= 1


def test_rank_sorted():
    e = HypothesisEngine(create("mock"))
    hyps = e.generate("question", n=3)
    ranked = e.rank(hyps)
    assert ranked[0].score >= ranked[-1].score
