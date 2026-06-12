#!/usr/bin/env python3
"""宿主 EngineAdapter 包注册（框架层不含任何具体游戏项目 import）。"""
from __future__ import annotations

import importlib
import os


def register_host_packages(packages: list[str]) -> list[str]:
    loaded: list[str] = []
    for raw in packages:
        name = raw.strip()
        if not name:
            continue
        importlib.import_module(name)
        loaded.append(name)
    return loaded


def packages_from_env() -> list[str]:
    raw = os.environ.get("FIGHT_ENTITY_HOST_PACKAGES", "")
    parts: list[str] = []
    for chunk in raw.replace(",", ";").split(";"):
        name = chunk.strip()
        if name:
            parts.append(name)
    return parts
