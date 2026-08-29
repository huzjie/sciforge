# -*- coding: utf-8 -*-
"""核心数据模型（纯 dataclass，零依赖）。"""
from __future__ import annotations

import enum
import time
import uuid
from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List, Optional


def _now() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%S")


def _uid(prefix: str = "") -> str:
    return prefix + uuid.uuid4().hex[:12]


class HypothesisStatus(str, enum.Enum):
    PROPOSED = "proposed"
    RANKED = "ranked"
    TESTED = "tested"
    CONFIRMED = "confirmed"
    REJECTED = "rejected"


class ExperimentStatus(str, enum.Enum):
    DRAFT = "draft"
    DESIGNED = "designed"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class ArtifactKind(str, enum.Enum):
    NOTEBOOK = "notebook"
    DATASET = "dataset"
    MODEL = "model"
    REPORT = "report"
    FIGURE = "figure"


@dataclass
class Hypothesis:
    statement: str
    rationale: str = ""
    score: float = 0.0
    source_refs: List[str] = field(default_factory=list)
    status: str = HypothesisStatus.PROPOSED.value
    tags: List[str] = field(default_factory=list)
    id: str = field(default_factory=lambda: _uid("hyp_"))
    created_at: str = field(default_factory=_now)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class LiteratureEntry:
    title: str
    authors: List[str] = field(default_factory=list)
    year: int = 0
    abstract: str = ""
    url: str = ""
    keywords: List[str] = field(default_factory=list)
    citations: int = 0
    id: str = field(default_factory=lambda: _uid("lit_"))
    created_at: str = field(default_factory=_now)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class ExperimentDesign:
    hypothesis_id: str
    independent_vars: List[str] = field(default_factory=list)
    dependent_vars: List[str] = field(default_factory=list)
    controls: List[str] = field(default_factory=list)
    method: str = ""
    protocol: str = ""
    sample_size: int = 0
    id: str = field(default_factory=lambda: _uid("exp_"))
    status: str = ExperimentStatus.DRAFT.value
    created_at: str = field(default_factory=_now)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class ExperimentResult:
    design_id: str
    observations: Dict[str, Any] = field(default_factory=dict)
    metrics: Dict[str, float] = field(default_factory=dict)
    conclusion: str = ""
    id: str = field(default_factory=lambda: _uid("res_"))
    status: str = ExperimentStatus.COMPLETED.value
    created_at: str = field(default_factory=_now)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class Artifact:
    kind: str
    content_hash: str
    parents: List[str] = field(default_factory=list)
    meta: Dict[str, Any] = field(default_factory=dict)
    id: str = field(default_factory=lambda: _uid("art_"))
    created_at: str = field(default_factory=_now)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class BenchmarkCase:
    name: str
    suite: str
    prompt: str
    reference: str = ""
    id: str = field(default_factory=lambda: _uid("bmc_"))

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class BenchmarkResult:
    case_id: str
    output: str = ""
    score: float = 0.0
    metrics: Dict[str, float] = field(default_factory=dict)
    id: str = field(default_factory=lambda: _uid("bmr_"))
    created_at: str = field(default_factory=_now)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


__all__ = [
    "HypothesisStatus", "ExperimentStatus", "ArtifactKind",
    "Hypothesis", "LiteratureEntry", "ExperimentDesign", "ExperimentResult",
    "Artifact", "BenchmarkCase", "BenchmarkResult",
]
