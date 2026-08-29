# -*- coding: utf-8 -*-
"""智能体生命周期状态机。"""
from __future__ import annotations

import enum
from typing import Dict, List


class AgentState(str, enum.Enum):
    IDLE = "idle"
    RESEARCHING = "researching"
    REVIEWING = "reviewing"
    DONE = "done"
    ERROR = "error"


_TRANSITIONS: Dict[AgentState, List[AgentState]] = {
    AgentState.IDLE: [AgentState.RESEARCHING, AgentState.ERROR],
    AgentState.RESEARCHING: [AgentState.REVIEWING, AgentState.ERROR],
    AgentState.REVIEWING: [AgentState.RESEARCHING, AgentState.DONE, AgentState.ERROR],
    AgentState.DONE: [],
    AgentState.ERROR: [AgentState.IDLE],
}


def transition(current: AgentState, target: AgentState) -> bool:
    return target in _TRANSITIONS.get(current, [])


__all__ = ["AgentState", "transition"]
