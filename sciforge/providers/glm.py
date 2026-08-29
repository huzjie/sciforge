# -*- coding: utf-8 -*-
"""智谱 GLM Provider（OpenAI 兼容端点）。"""
from __future__ import annotations

from .openai_compat import OpenAICompatProvider


class GLMProvider(OpenAICompatProvider):
    name = "glm"
    base_url = "https://open.bigmodel.cn/api/paas/v4"
    default_model = "glm-4-flash"
    env_key = "ZHIPU_API_KEY"


__all__ = ["GLMProvider"]
