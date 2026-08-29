# -*- coding: utf-8 -*-
"""Mock Provider：完全离线、确定性输出，用于端到端演示与测试。"""
from __future__ import annotations

import hashlib
from typing import Any, Dict, List

from .base import BaseProvider


class MockProvider(BaseProvider):
    name = "mock"

    def chat(self, messages: List[Dict[str, str]], **kwargs: Any) -> str:
        prompt = " ".join(m.get("content", "") for m in messages if isinstance(m, dict))
        return self._respond(prompt)

    def _respond(self, prompt: str) -> str:
        p = prompt.lower()
        # 顺序敏感：打分/实验/综述/评审 关键字需先于「假设」匹配
        if "rank" in p or "score" in p or "打分" in p:
            h = int(hashlib.sha256(prompt.encode("utf-8")).hexdigest()[:4], 16)
            return "%.3f" % (0.5 + (h % 350) / 1000.0)
        if "experiment" in p or "design" in p or "实验" in p:
            return ("独立变量：A；因变量：B；控制变量：C、D；"
                    "方法：随机对照试验；建议样本量 n=30。")
        if "summari" in p or "synthes" in p or "综合" in p or "评述" in p:
            return "综合来看，多项证据一致支持核心结论；尚存的分歧集中在方法与样本代表性上。"
        if "review" in p or "critique" in p or "peer" in p or "评审" in p or "批判" in p:
            return "建议补充对照组与效应量估计，方法总体可行，可进入下一轮验证。"
        if "stat" in p:
            return "t=2.31, p=0.032, cohen_d=0.84, 95%CI=[0.21, 1.47]"
        if "hypothes" in p or "假设" in p:
            q = self._question(prompt)
            return "\n".join([
                "若 %s 则结果 Y1：通过机制 M1 作用于通路 P1，预测效应显著（依据文献 L1）。" % q,
                "若 %s 则结果 Y2：通过机制 M2 调节通路 P2，预测存在剂量依赖（依据文献 L2）。" % q,
                "若 %s 则结果 Y3：通过机制 M3 反向影响通路 P3，预测在对照组中被抑制（依据文献 L3）。" % q,
            ])
        if "literature" in p or "search" in p or "文献" in p:
            return "相关文献集中在机制通路与临床转化两个方向，代表性工作见引文列表。"
        return "（mock 响应）" + prompt[:60]

    def _question(self, prompt: str) -> str:
        if "研究问题：" in prompt:
            rest = prompt.split("研究问题：", 1)[1]
            q = rest.split("\n")[0].strip()
            return q[:40] or "X"
        return "X"

    def healthcheck(self) -> bool:
        return True


__all__ = ["MockProvider"]
