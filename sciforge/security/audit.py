# -*- coding: utf-8 -*-
"""追加式 JSONL 审计日志。"""
from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any, Dict


class AuditLog:
    def __init__(self, path: str = "./data/audit.jsonl"):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def record(self, action: str, actor: str = "system", meta: Dict[str, Any] | None = None) -> None:
        entry = {
            "ts": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "action": action,
            "actor": actor,
            "meta": meta or {},
        }
        with open(self.path, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    def tail(self, n: int = 20) -> list:
        if not self.path.exists():
            return []
        lines = self.path.read_text(encoding="utf-8").splitlines()
        out = []
        for ln in lines[-n:]:
            try:
                out.append(json.loads(ln))
            except json.JSONDecodeError:
                continue
        return out


__all__ = ["AuditLog"]
