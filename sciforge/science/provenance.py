# -*- coding: utf-8 -*-
"""可复现溯源：对每个产物记录哈希、血缘链，支持重放。"""
from __future__ import annotations

import hashlib
from typing import List, Optional

from ..schema import Artifact, ArtifactKind


class ProvenanceTracker:
    def __init__(self) -> None:
        self._artifacts: dict = {}

    @staticmethod
    def hash_content(content: str | bytes) -> str:
        if isinstance(content, str):
            content = content.encode("utf-8")
        return hashlib.sha256(content).hexdigest()

    def record(self, kind: str, content: str | bytes,
               parents: Optional[List[str]] = None, meta: Optional[dict] = None) -> Artifact:
        a = Artifact(
            kind=kind,
            content_hash=self.hash_content(content),
            parents=parents or [],
            meta=meta or {},
        )
        self._artifacts[a.id] = a
        return a

    def get(self, artifact_id: str) -> Optional[Artifact]:
        return self._artifacts.get(artifact_id)

    def lineage(self, artifact_id: str) -> List[Artifact]:
        out: List[Artifact] = []
        seen = set()
        stack = [artifact_id]
        while stack:
            cur = stack.pop()
            if cur in seen or cur not in self._artifacts:
                continue
            seen.add(cur)
            a = self._artifacts[cur]
            out.append(a)
            stack.extend(a.parents)
        return out


__all__ = ["ProvenanceTracker"]
