# -*- coding: utf-8 -*-
"""文献检索与综述：检索相关文献、生成综合摘要。"""
from __future__ import annotations

from typing import List

from ..providers.base import BaseProvider
from ..schema import LiteratureEntry


class LiteratureSearch:
    def __init__(self, provider: BaseProvider):
        self.provider = provider

    def search(self, query: str, n: int = 5) -> List[LiteratureEntry]:
        # 离线兜底：基于关键词生成结构化文献条目（demo 用）
        entries = []
        for i in range(n):
            entries.append(LiteratureEntry(
                title="%s —— 相关研究综述（%d）" % (query, i + 1),
                authors=["样例作者"],
                year=2026 - i,
                abstract="围绕「%s」的机制、方法与结论综述。" % query,
                keywords=[w for w in query.replace("，", " ").split()[:4]],
            ))
        return entries

    def synthesize(self, entries: List[LiteratureEntry], question: str = "") -> str:
        titles = "\n".join("- %s" % e.title for e in entries[:10])
        prompt = "研究问题：%s\n\n相关文献：\n%s\n\n请给出综合评述（summary）。" % (question, titles)
        return self.provider.complete(prompt)


__all__ = ["LiteratureSearch"]
