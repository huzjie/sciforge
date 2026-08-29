# -*- coding: utf-8 -*-
"""本地 Ollama Provider（OpenAI 兼容端点）。"""
from __future__ import annotations

from .openai_compat import OpenAICompatProvider


class OllamaProvider(OpenAICompatProvider):
    name = "ollama"
    base_url = "http://localhost:11434/v1"
    default_model = "llama3.1"
    env_key = "OLLAMA_API_KEY"


__all__ = ["OllamaProvider"]
