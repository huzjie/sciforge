# -*- coding: utf-8 -*-
"""基于标准库 urllib 的 HTTP Provider 基类（零第三方依赖）。"""
from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from typing import Any, Dict, List, Optional

from ..errors import ProviderError
from .base import BaseProvider


class HttpProvider(BaseProvider):
    name = "http"
    base_url: str = ""
    default_model: str = ""
    env_key: str = ""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__(config)
        self.base_url = (self.config.get("base_url") or self.base_url).rstrip("/")
        self.model = self.config.get("model") or self.default_model
        self.api_key = self.config.get("api_key") or os.environ.get(self.env_key, "")

    def _build_request(self, messages: List[Dict[str, str]]) -> tuple:
        url = self.base_url + "/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + self.api_key,
        }
        payload = {"model": self.model, "messages": messages}
        return url, headers, payload

    def _extract_text(self, data: Dict[str, Any]) -> str:
        try:
            return data["choices"][0]["message"]["content"]
        except (KeyError, IndexError, TypeError):
            raise ProviderError("无法解析 provider 响应: %s" % str(data)[:200])

    def chat(self, messages: List[Dict[str, str]], **kwargs: Any) -> str:
        url, headers, payload = self._build_request(messages)
        payload.update(kwargs)
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(url, data=data, method="POST")
        for k, v in headers.items():
            req.add_header(k, v)
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                body = json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            raise ProviderError("HTTP %s: %s" % (e.code, e.read().decode("utf-8", "replace")[:300]))
        except urllib.error.URLError as e:
            raise ProviderError("网络错误: %s" % e.reason)
        return self._extract_text(body)


__all__ = ["HttpProvider"]
