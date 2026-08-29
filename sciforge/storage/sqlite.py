# -*- coding: utf-8 -*-
"""SQLite 存储（标准库 sqlite3，零依赖）。"""
from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Any, Dict, List, Optional

from ..errors import StorageError

_SCHEMA = """
CREATE TABLE IF NOT EXISTS hypotheses (
    id TEXT PRIMARY KEY, data TEXT NOT NULL, created_at TEXT
);
CREATE TABLE IF NOT EXISTS literature (
    id TEXT PRIMARY KEY, data TEXT NOT NULL, created_at TEXT
);
CREATE TABLE IF NOT EXISTS experiments (
    id TEXT PRIMARY KEY, data TEXT NOT NULL, created_at TEXT
);
CREATE TABLE IF NOT EXISTS artifacts (
    id TEXT PRIMARY KEY, data TEXT NOT NULL, created_at TEXT
);
"""


class SqliteStore:
    def __init__(self, path: str = "./data/sciforge.db"):
        self.path = path
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        self._conn = sqlite3.connect(path)
        self._conn.executescript(_SCHEMA)
        self._conn.commit()

    def _upsert(self, table: str, obj_id: str, data: Dict[str, Any]) -> None:
        payload = json.dumps(data, ensure_ascii=False)
        self._conn.execute(
            "INSERT OR REPLACE INTO %s (id, data, created_at) VALUES (?, ?, ?)" % table,
            (obj_id, payload, data.get("created_at", "")),
        )
        self._conn.commit()

    def _fetch(self, table: str, obj_id: Optional[str] = None) -> List[Dict[str, Any]]:
        if obj_id:
            rows = self._conn.execute(
                "SELECT data FROM %s WHERE id = ?" % table, (obj_id,)
            ).fetchall()
        else:
            rows = self._conn.execute("SELECT data FROM %s" % table).fetchall()
        return [json.loads(r[0]) for r in rows]

    def save_hypothesis(self, h: Dict[str, Any]) -> None:
        self._upsert("hypotheses", h["id"], h)

    def save_literature(self, e: Dict[str, Any]) -> None:
        self._upsert("literature", e["id"], e)

    def save_experiment(self, e: Dict[str, Any]) -> None:
        self._upsert("experiments", e["id"], e)

    def save_artifact(self, a: Dict[str, Any]) -> None:
        self._upsert("artifacts", a["id"], a)

    def get_hypotheses(self, obj_id: Optional[str] = None) -> List[Dict[str, Any]]:
        return self._fetch("hypotheses", obj_id)

    def get_literature(self, obj_id: Optional[str] = None) -> List[Dict[str, Any]]:
        return self._fetch("literature", obj_id)

    def get_experiments(self, obj_id: Optional[str] = None) -> List[Dict[str, Any]]:
        return self._fetch("experiments", obj_id)

    def close(self) -> None:
        self._conn.close()


__all__ = ["SqliteStore"]
