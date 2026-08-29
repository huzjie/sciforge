# -*- coding: utf-8 -*-
"""Provider 工厂与注册表。"""
from __future__ import annotations

from typing import Dict, List, Optional

from ..errors import ConfigError
from .base import BaseProvider
from .anthropic import AnthropicProvider
from .openai_compat import OpenAICompatProvider
from .deepseek import DeepSeekProvider
from .qwen import QwenProvider
from .kimi import KimiProvider
from .glm import GLMProvider
from .gemini import GeminiProvider
from .ollama import OllamaProvider
from .mock import MockProvider

REGISTRY: Dict[str, type] = {
    "openai": OpenAICompatProvider,
    "anthropic": AnthropicProvider,
    "gemini": GeminiProvider,
    "deepseek": DeepSeekProvider,
    "qwen": QwenProvider,
    "kimi": KimiProvider,
    "glm": GLMProvider,
    "ollama": OllamaProvider,
    "mock": MockProvider,
}


def available() -> List[str]:
    return sorted(REGISTRY.keys())


def create(name: str, config: Optional[dict] = None) -> BaseProvider:
    if name not in REGISTRY:
        raise ConfigError("未知 provider: %s (可用: %s)" % (name, ", ".join(available())))
    return REGISTRY[name](config or {})


__all__ = ["REGISTRY", "available", "create"]
