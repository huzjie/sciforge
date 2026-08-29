# -*- coding: utf-8 -*-
"""DeepSeek Provider（OpenAI 兼容端点）。"""
from __future__ import annotations

from .openai_compat import OpenAICompatProvider


class DeepSeekProvider(OpenAICompatProvider):
    name = "deepseek"
    base_url = "https://api.deepseek.com/v1"
    default_model = "deepseek-chat"
    env_key = "DEEPSEEK_API_KEY"


__all__ = ["DeepSeekProvider"]
