# -*- coding: utf-8 -*-
from sciforge.orchestrator import ResearchOrchestrator


def test_doctor():
    o = ResearchOrchestrator()
    d = o.doctor()
    assert d["provider"] == "mock"
    assert d["provider_ok"] is True


def test_run():
    o = ResearchOrchestrator()
    report = o.run("test research question")
    assert report.iterations >= 1
