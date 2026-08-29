# -*- coding: utf-8 -*-
from sciforge.providers import create, available


def test_all_providers_available():
    names = available()
    assert "mock" in names
    assert len(names) == 9


def test_all_providers_instantiate():
    for name in available():
        p = create(name)
        assert p.name == name


def test_mock_hypothesis():
    p = create("mock")
    out = p.complete("propose a hypothesis about sleep")
    assert "若" in out or "hypothesis" in out.lower() or "X" in out


def test_mock_score_is_number():
    p = create("mock")
    out = p.complete("请对该假设打分")
    assert float(out) >= 0.0
