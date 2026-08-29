# -*- coding: utf-8 -*-
from sciforge.agents import AgentState, transition, ROLES
from sciforge.agents.agent import Agent
from sciforge.providers import create


def test_roles_present():
    assert "scientist" in ROLES
    assert "reviewer" in ROLES


def test_transitions():
    assert transition(AgentState.IDLE, AgentState.RESEARCHING)
    assert transition(AgentState.RESEARCHING, AgentState.REVIEWING)


def test_agent_act():
    a = Agent(ROLES["scientist"], create("mock"))
    out = a.act("propose a hypothesis")
    assert out
