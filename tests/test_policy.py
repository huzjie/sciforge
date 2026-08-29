# -*- coding: utf-8 -*-
import pytest

from sciforge.errors import SecurityError
from sciforge.security.policy import PolicyEngine


def test_allow_run():
    p = PolicyEngine()
    assert p.authorize("run")


def test_deny_high_risk():
    p = PolicyEngine()
    assert not p.authorize("execute_os")


def test_guard_raises():
    p = PolicyEngine()
    with pytest.raises(SecurityError):
        p.guard("delete_all")
