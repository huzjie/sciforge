# -*- coding: utf-8 -*-
"""sciforge 统一异常体系。"""


class SciforgeError(Exception):
    """基础异常。"""


class ConfigError(SciforgeError):
    """配置加载 / 校验错误。"""


class ProviderError(SciforgeError):
    """LLM Provider 调用错误。"""


class HypothesisError(SciforgeError):
    """假设生成 / 排序错误。"""


class ExperimentError(SciforgeError):
    """实验设计 / 执行错误。"""


class StorageError(SciforgeError):
    """存储层错误。"""


class SecurityError(SciforgeError):
    """安全策略拒绝。"""


class ValidationError(SciforgeError):
    """数据校验错误。"""


__all__ = [
    "SciforgeError", "ConfigError", "ProviderError", "HypothesisError",
    "ExperimentError", "StorageError", "SecurityError", "ValidationError",
]
