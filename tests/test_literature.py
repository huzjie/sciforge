# -*- coding: utf-8 -*-
from sciforge.providers import create
from sciforge.science.literature import LiteratureSearch


def test_search():
    s = LiteratureSearch(create("mock"))
    entries = s.search("test query", n=5)
    assert len(entries) == 5


def test_synthesize():
    s = LiteratureSearch(create("mock"))
    text = s.synthesize(s.search("q", n=3))
    assert isinstance(text, str) and text
