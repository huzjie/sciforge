# -*- coding: utf-8 -*-
"""Google Gemini Provider（OpenAI 兼容端点）。"""
from __future__ import annotations

from .openai_compat import OpenAICompatProvider


class GeminiProvider(OpenAICompatProvider):
    name = "gemini"
    base_url = "https://generativelanguage.googleapis.com/v1beta/openai"
    default_model = "gemini-2.0-flash"
    env_key = "GEMINI_API_KEY"


__all__ = ["GeminiProvider"]
