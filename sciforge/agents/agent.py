# -*- coding: utf-8 -*-
"""科研智能体：绑定角色 + Provider，可独立执行子任务。"""
from __future__ import annotations

from ..providers.base import BaseProvider
from .lifecycle import AgentState, transition
from .roles import Role


class Agent:
    def __init__(self, role: Role, provider: BaseProvider):
        self.role = role
        self.provider = provider
        self.state = AgentState.IDLE

    def act(self, instruction: str) -> str:
        if not transition(self.state, AgentState.RESEARCHING):
            self.state = AgentState.RESEARCHING
        out = self.provider.chat([
            {"role": "system", "content": self.role.system_prompt},
            {"role": "user", "content": instruction},
        ])
        if transition(self.state, AgentState.REVIEWING):
            self.state = AgentState.REVIEWING
        return out

    def finish(self) -> None:
        self.state = AgentState.DONE


__all__ = ["Agent"]
