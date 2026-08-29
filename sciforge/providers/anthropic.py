# -*- coding: utf-8 -*-
"""Anthropic Claude Provider（原生 /v1/messages 协议）。"""
from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from typing import Any, Dict, List

from ..errors import ProviderError
from .base import BaseProvider


class AnthropicProvider(BaseProvider):
    name = "anthropic"
    base_url = "https://api.anthropic.com"
    default_model = "claude-sonnet-4-20250514"
    env_key = "ANTHROPIC_API_KEY"
    version = "2023-06-01"

    def __init__(self, config: Dict[str, Any] | None = None):
        super().__init__(config)
        self.base_url = (self.config.get("base_url") or self.base_url).rstrip("/")
        self.model = self.config.get("model") or self.default_model
        self.api_key = self.config.get("api_key") or os.environ.get(self.env_key, "")

    def chat(self, messages: List[Dict[str, str]], **kwargs: Any) -> str:
        system = " ".join(m.get("content", "") for m in messages if m.get("role") == "system")
        turns = [m for m in messages if m.get("role") != "system"]
        payload = {
            "model": self.model,
            "max_tokens": kwargs.get("max_tokens", 1024),
            "messages": turns,
        }
        if system:
            payload["system"] = system
        url = self.base_url + "/v1/messages"
        req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), method="POST")
        req.add_header("Content-Type", "application/json")
        req.add_header("x-api-key", self.api_key)
        req.add_header("anthropic-version", self.version)
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                body = json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            raise ProviderError("HTTP %s: %s" % (e.code, e.read().decode("utf-8", "replace")[:300]))
        except urllib.error.URLError as e:
            raise ProviderError("网络错误: %s" % e.reason)
        try:
            return "".join(b.get("text", "") for b in body["content"] if b.get("type") == "text")
        except (KeyError, TypeError):
            raise ProviderError("无法解析 Anthropic 响应: %s" % str(body)[:200])


__all__ = ["AnthropicProvider"]
