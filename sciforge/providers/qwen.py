# -*- coding: utf-8 -*-
"""通义千问 Qwen Provider（OpenAI 兼容端点）。"""
from __future__ import annotations

from .openai_compat import OpenAICompatProvider


class QwenProvider(OpenAICompatProvider):
    name = "qwen"
    base_url = "https://dashscope.aliyuncs.com/compatible-mode/v1"
    default_model = "qwen-plus"
    env_key = "DASHSCOPE_API_KEY"


__all__ = ["QwenProvider"]
