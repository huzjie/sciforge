# -*- coding: utf-8 -*-
"""sciforge 命令行入口。"""
from __future__ import annotations

import argparse
import json
import sys
from typing import List, Optional

from .version import __version__


def _orch():
    from .orchestrator import ResearchOrchestrator
    return ResearchOrchestrator()


def cmd_version(args) -> int:
    print("sciforge %s" % __version__)
    return 0


def cmd_doctor(args) -> int:
    orch = _orch()
    print(json.dumps(orch.doctor(), ensure_ascii=False, indent=2))
    return 0


def cmd_hypothesize(args) -> int:
    from .science.hypothesis import HypothesisEngine
    orch = _orch()
    hyps = HypothesisEngine(orch.provider).generate(args.question, args.n)
    ranked = HypothesisEngine(orch.provider).rank(hyps, args.question)
    for i, h in enumerate(ranked, 1):
        print("%d. [%.3f] %s" % (i, h.score, h.statement))
    return 0


def cmd_search(args) -> int:
    from .science.literature import LiteratureSearch
    orch = _orch()
    entries = LiteratureSearch(orch.provider).search(args.query, args.n)
    for e in entries:
        print("- %s (%d)" % (e.title, e.year))
    return 0


def cmd_design(args) -> int:
    from .schema import Hypothesis
    from .science.experiment import ExperimentDesigner
    orch = _orch()
    d = ExperimentDesigner(orch.provider).design(Hypothesis(statement=args.statement))
    print(json.dumps(d.to_dict(), ensure_ascii=False, indent=2))
    return 0


def cmd_run(args) -> int:
    orch = _orch()
    report = orch.run(args.question)
    print(json.dumps(report.to_dict(), ensure_ascii=False, indent=2))
    return 0


def cmd_benchmark(args) -> int:
    orch = _orch()
    results = orch.benchmark.run(args.suite or "")
    total = sum(r.score for r in results)
    print("suite=%s cases=%d avg_score=%.4f" %
          (args.suite or "all", len(results), total / len(results) if results else 0))
    for r in results:
        print("  [%.4f] %s" % (r.score, r.case_id))
    return 0


def cmd_reproduce(args) -> int:
    from .science.provenance import ProvenanceTracker
    pt = ProvenanceTracker()
    content = "示例产物内容"
    a = pt.record("report", content)
    print("artifact_id=%s sha256=%s" % (a.id, a.content_hash))
    return 0


def cmd_serve(args) -> int:
    host = args.host
    port = args.port
    try:
        from .api.app import create_app
        import uvicorn  # noqa
        app = create_app()
        uvicorn.run(app, host=host, port=port, log_level="info")
    except ImportError:
        # FastAPI/uvicorn 未安装 -> 纯标准库兜底
        from .api.stdlib_server import run_server
        print("[serve] FastAPI 不可用，使用纯标准库 HTTP 服务")
        run_server(host=host, port=port)
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="sciforge", description="AI 科研智能体与自动化科学发现平台")
    p.add_argument("--version", action="store_true", help="打印版本")
    sub = p.add_subparsers(dest="command")

    sp = sub.add_parser("doctor", help="自检")
    sp.set_defaults(func=cmd_doctor)

    sp = sub.add_parser("hypothesize", help="生成并排序假设")
    sp.add_argument("question")
    sp.add_argument("-n", type=int, default=3)
    sp.set_defaults(func=cmd_hypothesize)

    sp = sub.add_parser("search", help="检索文献")
    sp.add_argument("query")
    sp.add_argument("-n", type=int, default=5)
    sp.set_defaults(func=cmd_search)

    sp = sub.add_parser("design", help="设计实验")
    sp.add_argument("statement")
    sp.set_defaults(func=cmd_design)

    sp = sub.add_parser("run", help="运行完整研究闭环")
    sp.add_argument("question")
    sp.set_defaults(func=cmd_run)

    sp = sub.add_parser("benchmark", help="运行基准评测")
    sp.add_argument("--suite", default="")
    sp.set_defaults(func=cmd_benchmark)

    sp = sub.add_parser("reproduce", help="演示可复现溯源")
    sp.set_defaults(func=cmd_reproduce)

    sp = sub.add_parser("serve", help="启动控制面服务")
    sp.add_argument("--host", default="0.0.0.0")
    sp.add_argument("--port", type=int, default=8000)
    sp.set_defaults(func=cmd_serve)

    return p


def main(argv: Optional[List[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.version:
        return cmd_version(args)
    if not getattr(args, "command", None):
        parser.print_help()
        return 0
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
