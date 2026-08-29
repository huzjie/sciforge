# -*- coding: utf-8 -*-
"""纯标准库 HTTP 控制面（无 FastAPI 时的兜底实现）。"""
from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

from ..orchestrator import ResearchOrchestrator
from ..version import __version__


def _make_app():
    orch = ResearchOrchestrator()
    routes = {
        "/healthz": lambda: {"status": "ok", "version": __version__},
        "/version": lambda: {"version": __version__},
        "/doctor": lambda: orch.doctor(),
        "/metrics": lambda: {"metrics": orch.metrics.render()},
    }
    return orch, routes


class _Handler(BaseHTTPRequestHandler):
    orch = None
    routes = None

    def _send(self, code: int, obj) -> None:
        body = json.dumps(obj, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        if path in self.routes:
            self._send(200, self.routes[path]())
        elif path == "/benchmarks":
            suite = parse_qs(parsed.query).get("suite", [""])[0]
            self._send(200, [r.to_dict() for r in self.orch.benchmark.run(suite)])
        else:
            self._send(404, {"error": "not found"})

    def do_POST(self):
        parsed = urlparse(self.path)
        if parsed.path == "/research":
            length = int(self.headers.get("Content-Length", 0))
            raw = self.rfile.read(length).decode("utf-8")
            question = json.loads(raw).get("question", "")
            report = self.orch.run(question)
            self._send(200, report.to_dict())
        else:
            self._send(404, {"error": "not found"})

    def log_message(self, *args):
        pass


def run_server(host: str = "0.0.0.0", port: int = 8000) -> None:
    orch, routes = _make_app()
    _Handler.orch = orch
    _Handler.routes = routes
    server = HTTPServer((host, port), _Handler)
    print("[serve] stdlib server at http://%s:%d" % (host, port))
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.server_close()


__all__ = ["run_server"]
