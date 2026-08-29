# -*- coding: utf-8 -*-
"""多智能体科研角色定义。"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Role:
    key: str
    name: str
    system_prompt: str


ROLES = {
    "scientist": Role("scientist", "科学家", "你提出并检验可证伪的科学假设，严谨推理。"),
    "reviewer": Role("reviewer", "审稿人", "你以严格同行评审标准批判性审视每一项结论。"),
    "statistician": Role("statistician", "统计学家", "你负责实验设计与统计推断，警惕伪相关。"),
    "librarian": Role("librarian", "文献员", "你检索与综述文献，追溯证据来源。"),
    "labtech": Role("labtech", "实验员", "你规范执行实验流程，如实记录观察数据。"),
}


__all__ = ["ROLES", "Role"]
