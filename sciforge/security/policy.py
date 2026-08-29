# -*- coding: utf-8 -*-
"""安全策略引擎：按规则顺序首个匹配，默认拒绝（default-deny）。"""
from __future__ import annotations

from typing import Any, Dict, List

from ..errors import SecurityError

# 规则顺序即优先级：越靠前越先匹配；block 类规则必须前置。
DEFAULT_RULES: List[Dict[str, Any]] = [
    {"name": "block-high-risk", "action": "deny",
     "match": {"action": ["execute_os", "rm", "delete_all", "network_egress"]}},
    {"name": "block-oversized", "action": "deny",
     "match": {"artifact_bytes_gt": 10485760}},
    {"name": "allow-run", "action": "allow",
     "match": {"action": ["run", "research", "hypothesize", "search", "design", "benchmark"]}},
    {"name": "allow-read", "action": "allow",
     "match": {"action": ["read", "list", "get", "reproduce", "serve", "doctor"]}},
]


class PolicyEngine:
    def __init__(self, rules: List[Dict[str, Any]] | None = None):
        self.rules = rules or DEFAULT_RULES

    def authorize(self, action: str, context: Dict[str, Any] | None = None) -> bool:
        ctx = context or {}
        for rule in self.rules:
            if self._matches(rule.get("match", {}), action, ctx):
                return rule.get("action") == "allow"
        return False

    def _matches(self, match: Dict[str, Any], action: str, ctx: Dict[str, Any]) -> bool:
        if "action" in match and action not in match["action"]:
            return False
        if "artifact_bytes_gt" in match:
            size = ctx.get("artifact_bytes", 0)
            if size <= match["artifact_bytes_gt"]:
                return False
        if "require_tag" in match and match["require_tag"] not in ctx.get("tags", []):
            return False
        return True

    def guard(self, action: str, context: Dict[str, Any] | None = None) -> None:
        if not self.authorize(action, context):
            raise SecurityError("安全策略拒绝操作: %s" % action)


__all__ = ["PolicyEngine", "DEFAULT_RULES"]
