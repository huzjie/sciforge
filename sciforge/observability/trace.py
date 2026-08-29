# -*- coding: utf-8 -*-
"""W3C traceparent 分布式追踪上下文。"""
from __future__ import annotations

import random
import string
from typing import Optional


def _hex(n: int) -> str:
    return ("%032x" % n)


def _rand_hex(nbytes: int) -> str:
    return "".join(random.choice(string.hexdigits.lower()) for _ in range(nbytes * 2))


class TraceContext:
    def __init__(self, trace_id: Optional[str] = None, span_id: Optional[str] = None,
                 sampled: bool = True):
        self.trace_id = trace_id or _rand_hex(16)
        self.span_id = span_id or _rand_hex(8)
        self.sampled = sampled

    @classmethod
    def from_header(cls, header: str) -> "TraceContext":
        parts = header.split("-")
        if len(parts) >= 3:
            return cls(parts[1], _rand_hex(8), parts[2].startswith("01"))
        return cls()

    def child(self) -> "TraceContext":
        return TraceContext(self.trace_id, _rand_hex(8), self.sampled)

    def to_header(self) -> str:
        flags = "01" if self.sampled else "00"
        return "00-%s-%s-%s" % (self.trace_id, self.span_id, flags)


__all__ = ["TraceContext"]
