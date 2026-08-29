# -*- coding: utf-8 -*-
"""同行评审器：对假设 / 结果给出批判性意见。"""
from __future__ import annotations

from ..providers.base import BaseProvider


class PeerReviewer:
    def __init__(self, provider: BaseProvider):
        self.provider = provider

    def review(self, content: str) -> str:
        prompt = "请以严格同行评审的口吻，对以下内容给出批判性意见与改进建议：\n%s" % content
        return self.provider.complete(prompt)


__all__ = ["PeerReviewer"]
