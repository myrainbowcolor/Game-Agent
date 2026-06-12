#!/usr/bin/env python3
"""引擎适配器契约（EngineAdapter）。

自研 / Unity / UE 等各实现一套 adapter；Agent 主链只调本模块注册的实现。
"""
from __future__ import annotations

import json
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class PhaseResult:
    phase_id: str
    exit_code: int
    write_set: list[str] = field(default_factory=list)
    messages: list[str] = field(default_factory=list)
    gaps: list[dict[str, Any]] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return self.exit_code == 0


class EngineAdapter(ABC):
    """六个钩子对应最小闭环；子类可按引擎增减内部步骤。"""

    profile_id: str = "stub_engine"

    def __init__(self, client_root: Path) -> None:
        self.client_root = client_root.resolve()

    @abstractmethod
    def preflight_logic_asset(self, spec: dict[str, Any], entity_id: int) -> PhaseResult:
        """P-PREFAB：逻辑体/预制体预检或触发生成。"""

    @abstractmethod
    def generate_main_entity(self, spec: dict[str, Any], entity_id: int) -> PhaseResult:
        """P-ENTITY：主实体配置落盘。"""

    @abstractmethod
    def generate_derived(self, spec: dict[str, Any], entity_id: int) -> PhaseResult:
        """P-DERIVED-ENTITY。"""

    @abstractmethod
    def wire_skills(self, spec: dict[str, Any], entity_id: int) -> PhaseResult:
        """P-SKILL + 与 magic/派生衔接（引擎内可拆多步）。"""

    @abstractmethod
    def export_runtime(self, spec: dict[str, Any], entity_id: int) -> PhaseResult:
        """P-PRELOAD / P-TABLE：导表、运行时资源、后处理。"""

    @abstractmethod
    def verify(self, spec: dict[str, Any], entity_id: int) -> PhaseResult:
        """P-VERIFY：终局门禁。"""

    def run_pipeline(self, spec: dict[str, Any], entity_id: int) -> list[PhaseResult]:
        steps = [
            ("P-PREFAB", self.preflight_logic_asset),
            ("P-ENTITY", self.generate_main_entity),
            ("P-DERIVED-ENTITY", self.generate_derived),
            ("P-SKILL", self.wire_skills),
            ("P-EXPORT", self.export_runtime),
            ("P-VERIFY", self.verify),
        ]
        results: list[PhaseResult] = []
        for phase_id, fn in steps:
            res = fn(spec, entity_id)
            if res.phase_id != phase_id:
                res = PhaseResult(
                    phase_id=phase_id,
                    exit_code=res.exit_code,
                    write_set=res.write_set,
                    messages=res.messages,
                    gaps=res.gaps,
                )
            results.append(res)
            for m in res.messages:
                print(f"[{phase_id}] {m}")
            if not res.ok:
                break
        return results


_REGISTRY: dict[str, type[EngineAdapter]] = {}


def register_adapter(cls: type[EngineAdapter]) -> type[EngineAdapter]:
    _REGISTRY[cls.profile_id] = cls
    return cls


def get_adapter(profile: str, client_root: Path) -> EngineAdapter:
    pid = (profile or "stub_engine").strip()
    if pid not in _REGISTRY:
        known = ", ".join(sorted(_REGISTRY)) or "(none)"
        raise KeyError(f"未知 pipeline_profile={pid!r}；已注册: {known}")
    return _REGISTRY[pid](client_root)


def load_spec(spec_path: Path, entity_id: int) -> dict[str, Any]:
    data = json.loads(spec_path.read_text(encoding="utf-8-sig"))
    if not isinstance(data, dict):
        raise ValueError("spec root must be object")
    sid = data.get("entity_id")
    if sid is not None and int(sid) != int(entity_id):
        raise ValueError(f"spec entity_id={sid} != --entity-id {entity_id}")
    data.setdefault("entity_id", int(entity_id))
    data.setdefault("pipeline_profile", "stub_engine")
    return data
