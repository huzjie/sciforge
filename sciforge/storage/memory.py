# -*- coding: utf-8 -*-
"""内存存储（进程内 dict），用于无持久化场景。"""
from __future__ import annotations

from typing import Any, Dict, List, Optional


class MemoryStore:
    def __init__(self) -> None:
        self._data: Dict[str, Dict[str, Any]] = {}

    def put(self, collection: str, obj_id: str, data: Dict[str, Any]) -> None:
        self._data.setdefault(collection, {})[obj_id] = data

    def get(self, collection: str, obj_id: str) -> Optional[Dict[str, Any]]:
        return self._data.get(collection, {}).get(obj_id)

    def list(self, collection: str) -> List[Dict[str, Any]]:
        return list(self._data.get(collection, {}).values())

    def delete(self, collection: str, obj_id: str) -> None:
        self._data.get(collection, {}).pop(obj_id, None)


__all__ = ["MemoryStore"]
