# -*- coding: utf-8 -*-
from sciforge.config import load_config


def test_default_provider_is_mock():
    cfg = load_config()
    assert cfg["provider"] == "mock"


def test_researcher_settings():
    cfg = load_config()
    assert cfg["researcher"]["max_iterations"] > 0
