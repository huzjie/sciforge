# -*- coding: utf-8 -*-
from sciforge.science.statistics import StatisticalAnalyzer as S


def test_mean():
    assert S.mean([1, 2, 3]) == 2.0


def test_cohens_d_positive():
    d = S.cohens_d([2, 3, 4], [1, 1, 1])
    assert d > 0


def test_welch_t_p_in_range():
    t, p = S.welch_t([2, 3, 4, 5], [1, 1, 2, 1])
    assert 0.0 <= p <= 1.0
