# -*- coding: utf-8 -*-
"""月之暗面 Kimi Provider（OpenAI 兼容端点）。"""
from __future__ import annotations

from .openai_compat import OpenAICompatProvider


class KimiProvider(OpenAICompatProvider):
    name = "kimi"
    base_url = "https://api.moonshot.cn/v1"
    default_model = "moonshot-v1-8k"
    env_key = "MOONSHOT_API_KEY"


__all__ = ["KimiProvider"]
