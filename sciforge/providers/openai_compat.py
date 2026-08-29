# -*- coding: utf-8 -*-
"""OpenAI 兼容 Provider（默认 OpenAI，可作基类复用）。"""
from __future__ import annotations

from .http import HttpProvider


class OpenAICompatProvider(HttpProvider):
    name = "openai"
    base_url = "https://api.openai.com/v1"
    default_model = "gpt-4o-mini"
    env_key = "OPENAI_API_KEY"


__all__ = ["OpenAICompatProvider"]
