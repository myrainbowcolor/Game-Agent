#!/usr/bin/env python3
"""真源 Intake：Excel / CSV / JSON → spec（v0 桩 + JSON 直读）。"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def intake_to_spec(
    input_path: Path,
    entity_id: int,
    *,
    pipeline_profile: str = "stub_engine",
) -> dict[str, Any]:
    """按扩展名选择 adapter；未知格式抛错。"""
    p = input_path.resolve()
    if not p.is_file():
        raise FileNotFoundError(p)
    suf = p.suffix.lower()
    if suf == ".json":
        return _intake_json(p, entity_id, pipeline_profile)
    if suf in (".csv",):
        return _intake_stub_table(p, entity_id, pipeline_profile, format_name="csv")
    if suf in (".xlsx", ".xls"):
        return _intake_stub_table(p, entity_id, pipeline_profile, format_name="xlsx")
    raise ValueError(f"intake 未实现格式: {suf}（可扩展 fight_entity_core/intake.py）")


def _intake_json(path: Path, entity_id: int, profile: str) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(data, dict):
        raise ValueError("JSON 根须为 object")
    if "entity_id" in data and int(data["entity_id"]) != int(entity_id):
        raise ValueError("JSON entity_id 与参数不一致")
    data.setdefault("entity_id", int(entity_id))
    data.setdefault("pipeline_profile", profile)
    data.setdefault("skills", [])
    data.setdefault("derived", [])
    data.setdefault("gaps", [])
    return data


def _intake_stub_table(
    path: Path,
    entity_id: int,
    profile: str,
    *,
    format_name: str,
) -> dict[str, Any]:
    """表类真源占位：仅生成可继续管线化的 spec 骨架，具体映射由项目 adapter 实现。"""
    return {
        "entity_id": int(entity_id),
        "pipeline_profile": profile,
        "name_zh": "",
        "skills": [],
        "derived": [],
        "table_patches": [],
        "gaps": [
            {
                "kind": "intake_stub",
                "severity": "warn",
                "message": (
                    f"表类真源 {format_name} 仅生成骨架；"
                    f"请实现 intake 映射或改用 JSON spec：{path.name}"
                ),
            }
        ],
        "_meta": {
            "intake_source": str(path),
            "intake_format": format_name,
        },
    }
