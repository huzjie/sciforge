# -*- coding: utf-8 -*-
"""配置加载：内置默认值 -> config.json 覆盖 -> SCIFORGE_* 环境变量覆盖。

零第三方依赖。环境变量名用双下划线表示层级，例如：:

    SCIFORGE_PROVIDER=mock
    SCIFORGE_PROVIDERS__OPENAI__API_KEY=sk-...
    SCIFORGE_RESEARCHER__MAX_ITERATIONS=50
"""
from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Dict

from .errors import ConfigError

DEFAULT_CONFIG: Dict[str, Any] = {
    "provider": "mock",
    "providers": {
        "openai": {"base_url": "https://api.openai.com/v1", "model": "gpt-4o-mini", "api_key": ""},
        "anthropic": {"base_url": "https://api.anthropic.com", "model": "claude-sonnet-4-20250514", "api_key": ""},
        "gemini": {"base_url": "https://generativelanguage.googleapis.com/v1beta/openai", "model": "gemini-2.0-flash", "api_key": ""},
        "deepseek": {"base_url": "https://api.deepseek.com/v1", "model": "deepseek-chat", "api_key": ""},
        "qwen": {"base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1", "model": "qwen-plus", "api_key": ""},
        "kimi": {"base_url": "https://api.moonshot.cn/v1", "model": "moonshot-v1-8k", "api_key": ""},
        "glm": {"base_url": "https://open.bigmodel.cn/api/paas/v4", "model": "glm-4-flash", "api_key": ""},
        "ollama": {"base_url": "http://localhost:11434/v1", "model": "llama3.1", "api_key": ""},
        "mock": {"base_url": "", "model": "mock", "api_key": ""},
    },
    "researcher": {
        "max_iterations": 30,
        "cycle_minutes": 30,
        "hypotheses_per_cycle": 3,
        "convergence_threshold": 0.02,
        "auto_refine": True,
    },
    "benchmark": {
        "suites": ["hypothesis", "literature", "experiment", "reasoning"],
        "scoring": "rubric",
    },
    "storage": {"path": "./data/sciforge.db", "in_memory": False},
    "security": {"default_deny": True, "max_artifact_bytes": 10485760},
    "server": {"host": "0.0.0.0", "port": 8000},
    "logging": {"level": "INFO"},
}


def _deep_merge(base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
    out = dict(base)
    for k, v in (override or {}).items():
        if isinstance(v, dict) and isinstance(out.get(k), dict):
            out[k] = _deep_merge(out[k], v)
        else:
            out[k] = v
    return out


def _coerce(value: str) -> Any:
    s = value.strip()
    if s == "":
        return s
    low = s.lower()
    if low in ("true", "false"):
        return low == "true"
    if low in ("null", "none"):
        return None
    try:
        return int(s)
    except ValueError:
        pass
    try:
        return float(s)
    except ValueError:
        pass
    return s


def _apply_env(cfg: Dict[str, Any]) -> Dict[str, Any]:
    out = dict(cfg)
    for key, value in os.environ.items():
        if not key.startswith("SCIFORGE_"):
            continue
        parts = key[len("SCIFORGE_"):].lower().split("__")
        node = out
        for part in parts[:-1]:
            node = node.setdefault(part, {})
        node[parts[-1]] = _coerce(value)
    return out


def load_config(path: str = "config.json") -> Dict[str, Any]:
    """加载配置：默认 -> 文件 -> 环境变量。"""
    cfg = _deep_merge(DEFAULT_CONFIG, {})

    candidates = [path, "config.json", "config.example.json"]
    for cand in candidates:
        p = Path(cand)
        if p.exists():
            try:
                with open(p, "r", encoding="utf-8") as f:
                    cfg = _deep_merge(cfg, json.load(f))
                break
            except (json.JSONDecodeError, OSError) as exc:
                raise ConfigError("无法解析配置文件 %s: %s" % (cand, exc)) from exc

    cfg = _apply_env(cfg)
    _validate(cfg)
    return cfg


def _validate(cfg: Dict[str, Any]) -> None:
    if not isinstance(cfg.get("provider"), str):
        raise ConfigError("provider 必须是字符串")
    if cfg["provider"] not in cfg.get("providers", {}):
        raise ConfigError("provider 未在 providers 中注册: %s" % cfg["provider"])
    if not isinstance(cfg.get("researcher", {}).get("max_iterations"), int):
        raise ConfigError("researcher.max_iterations 必须是整数")


__all__ = ["load_config", "DEFAULT_CONFIG"]
