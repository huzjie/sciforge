# -*- coding: utf-8 -*-
"""sciforge Python SDK：本地进程内调用 + 可选 HTTP 远程客户端。"""
from __future__ import annotations

import json
import urllib.request
from typing import Any, Dict, Optional


class SciforgeClient:
    """SDK 客户端。不传 base_url 时进程内直连编排器。"""

    def __init__(self, base_url: Optional[str] = None):
        self.base_url = (base_url or "").rstrip("/")
        self._orch = None

    def _local(self):
        if self._orch is None:
            from .orchestrator import ResearchOrchestrator
            self._orch = ResearchOrchestrator()
        return self._orch

    def research(self, question: str) -> Dict[str, Any]:
        if self.base_url:
            return self._http_post("/research", {"question": question})
        return self._local().run(question).to_dict()

    def doctor(self) -> Dict[str, Any]:
        if self.base_url:
            return self._http_get("/doctor")
        return self._local().doctor()

    def benchmark(self, suite: str = "") -> list:
        if self.base_url:
            return self._http_get("/benchmarks?suite=" + suite)
        return [r.to_dict() for r in self._local().benchmark.run(suite)]

    def _http_get(self, path: str) -> Any:
        with urllib.request.urlopen(self.base_url + path, timeout=30) as r:
            return json.loads(r.read().decode("utf-8"))

    def _http_post(self, path: str, payload: dict) -> Any:
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(self.base_url + path, data=data, method="POST")
        req.add_header("Content-Type", "application/json")
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.loads(r.read().decode("utf-8"))


__all__ = ["SciforgeClient"]
