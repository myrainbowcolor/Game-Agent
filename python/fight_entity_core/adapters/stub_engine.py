#!/usr/bin/env python3
"""自研/未知引擎：桩 adapter（验证编排与打包，不写真实引擎文件）。"""
from __future__ import annotations

from pathlib import Path
from typing import Any

from fight_entity_core.adapter import EngineAdapter, PhaseResult, register_adapter


@register_adapter
class StubEngineAdapter(EngineAdapter):
    profile_id = "stub_engine"

    def _out_dir(self, entity_id: int) -> Path:
        d = self.client_root / "tmp" / "fight-entity-core-out" / str(entity_id)
        d.mkdir(parents=True, exist_ok=True)
        return d

    def preflight_logic_asset(self, spec: dict[str, Any], entity_id: int) -> PhaseResult:
        return PhaseResult(
            "P-PREFAB",
            0,
            messages=[f"stub: preflight ok (prefab={spec.get('prefab', '')!r})"],
        )

    def generate_main_entity(self, spec: dict[str, Any], entity_id: int) -> PhaseResult:
        out = self._out_dir(entity_id) / f"{entity_id}.main.json"
        import json

        out.write_text(json.dumps(spec, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        return PhaseResult("P-ENTITY", 0, write_set=[str(out)], messages=[f"stub: wrote {out}"])

    def generate_derived(self, spec: dict[str, Any], entity_id: int) -> PhaseResult:
        n = len(spec.get("derived") or [])
        return PhaseResult("P-DERIVED-ENTITY", 0, messages=[f"stub: derived count={n}"])

    def wire_skills(self, spec: dict[str, Any], entity_id: int) -> PhaseResult:
        n = len(spec.get("skills") or [])
        return PhaseResult("P-SKILL", 0, messages=[f"stub: skills count={n}"])

    def export_runtime(self, spec: dict[str, Any], entity_id: int) -> PhaseResult:
        patches = spec.get("table_patches") or []
        return PhaseResult(
            "P-EXPORT",
            0,
            messages=[f"stub: table_patches={len(patches)} (no-op export)"],
        )

    def verify(self, spec: dict[str, Any], entity_id: int) -> PhaseResult:
        main = self._out_dir(entity_id) / f"{entity_id}.main.json"
        if not main.is_file():
            return PhaseResult("P-VERIFY", 2, messages=["stub: main artifact missing"])
        return PhaseResult("P-VERIFY", 0, messages=["stub: pipeline_converged=true"])
