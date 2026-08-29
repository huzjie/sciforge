# -*- coding: utf-8 -*-
"""FastAPI 控制面（可选依赖；无 FastAPI 时由 stdlib_server 兜底）。"""
from __future__ import annotations

from typing import Any, Dict


def create_app():
    try:
        from fastapi import FastAPI
        from pydantic import BaseModel
    except ImportError as e:  # pragma: no cover
        raise RuntimeError("FastAPI 未安装，请使用纯标准库服务") from e

    from ..orchestrator import ResearchOrchestrator
    from ..version import __version__

    app = FastAPI(title="sciforge", version=__version__)
    orch = ResearchOrchestrator()

    class Question(BaseModel):
        question: str

    @app.get("/healthz")
    def healthz():
        return {"status": "ok", "version": __version__}

    @app.get("/version")
    def version():
        return {"version": __version__}

    @app.get("/doctor")
    def doctor():
        return orch.doctor()

    @app.post("/research")
    def research(q: Question):
        report = orch.run(q.question)
        return report.to_dict()

    @app.get("/benchmarks")
    def benchmarks(suite: str = ""):
        return [r.to_dict() for r in orch.benchmark.run(suite)]

    @app.get("/metrics")
    def metrics():
        return orch.metrics.render()

    return app


__all__ = ["create_app"]
