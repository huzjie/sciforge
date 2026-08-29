# -*- coding: utf-8 -*-
"""Provider 抽象基类。"""
from __future__ import annotations

from typing import Any, Dict, List, Optional


class BaseProvider:
    name: str = "base"

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}

    def chat(self, messages: List[Dict[str, str]], **kwargs: Any) -> str:
        raise NotImplementedError

    def complete(self, prompt: str, **kwargs: Any) -> str:
        return self.chat([{"role": "user", "content": prompt}], **kwargs)

    def healthcheck(self) -> bool:
        return True


__all__ = ["BaseProvider"]
