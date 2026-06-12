#!/usr/bin/env python3
"""引擎无关战斗实体管线入口（读 spec → 选 EngineAdapter → 跑 Phase）。

示例:
  python tools/run_fight_entity_pipeline.py --entity-id 9000001 --profile stub_engine
  python tools/run_fight_entity_pipeline.py --entity-id 6010300 --profile unity_wangyue
  python tools/run_fight_entity_pipeline.py --intake path/to/spec.json --entity-id 9000001
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

_TOOLS = Path(__file__).resolve().parent
if str(_TOOLS) not in sys.path:
    sys.path.insert(0, str(_TOOLS))

import fight_entity_core.adapters  # noqa: F401 — stub adapter

def _register_host_adapters() -> None:
    try:
        import fight_entity_host_wangyue  # noqa: F401 — 望月宿主，非框架仓
    except ImportError:
        pass

_register_host_adapters()
from fight_entity_core.adapter import get_adapter, load_spec
from fight_entity_core.intake import intake_to_spec


def _client_root() -> Path:
    return _TOOLS.parent


def _default_spec_path(entity_id: int) -> Path:
    return (
        _client_root()
        / "docs"
        / "knowledge"
        / "runtime"
        / "spec-cache"
        / f"{entity_id}.spec.json"
    )


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--entity-id", type=int, required=True)
    ap.add_argument(
        "--profile",
        type=str,
        default="",
        help="EngineAdapter profile：stub_engine | unity_wangyue | 自研注册名",
    )
    ap.add_argument("--spec", type=str, default="", help="spec.json 路径")
    ap.add_argument("--intake", type=str, default="", help="真源 intake（json/csv/xlsx 桩）")
    ap.add_argument("--write-spec", action="store_true", help="intake 后写回 spec-cache")
    args = ap.parse_args()

    root = _client_root()
    eid = int(args.entity_id)
    profile = (args.profile or "").strip()

    if args.intake:
        spec = intake_to_spec(
            Path(args.intake),
            eid,
            pipeline_profile=profile or "stub_engine",
        )
        if args.write_spec:
            sp = _default_spec_path(eid)
            sp.parent.mkdir(parents=True, exist_ok=True)
            sp.write_text(json.dumps(spec, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            print(f"[ok] spec written: {sp}")
    else:
        sp = Path(args.spec).resolve() if args.spec else _default_spec_path(eid)
        if not sp.is_file():
            print(f"[error] spec not found: {sp}", file=sys.stderr)
            return 1
        spec = load_spec(sp, eid)

    profile = profile or str(spec.get("pipeline_profile") or "stub_engine")
    adapter = get_adapter(profile, root)
    print(f"[pipeline] profile={profile} adapter={adapter.__class__.__name__} entity_id={eid}")

    results = adapter.run_pipeline(spec, eid)
    bad = next((r for r in results if not r.ok), None)
    if bad:
        print(
            f"[pipeline-ledger] converged=false phase={bad.phase_id} exit={bad.exit_code}",
            file=sys.stderr,
        )
        return bad.exit_code if bad.exit_code != 0 else 1
    print("[pipeline-ledger] converged=true")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
