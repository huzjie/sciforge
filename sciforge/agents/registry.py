# -*- coding: utf-8 -*-
from .roles import ROLES, Role


class RoleRegistry:
    @staticmethod
    def get(key: str) -> Role:
        return ROLES[key]

    @staticmethod
    def list_keys() -> list:
        return sorted(ROLES.keys())


__all__ = ["RoleRegistry"]
