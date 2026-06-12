#!/usr/bin/env python3
"""框架 CLI 内核：intake/spec → EngineAdapter → pipeline-ledger。"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import fight_entity_core.adapters  # noqa: F401 — stub adapter
from fight_entity_core.adapter import get_adapter, load_spec
from fight_entity_core.host_loader import packages_from_env, register_host_packages
from fight_entity_core.intake import intake_to_spec


def project_root(tools_dir: Path) -> Path:
    return tools_dir.parent.resolve()


def build_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(
        description="引擎无关战斗实体管线：读 spec → 选 EngineAdapter → 跑 Phase。",
    )
    ap.add_argument("--entity-id", type=int, required=True)
    ap.add_argument(
        "--profile",
        type=str,
        default="",
        help="EngineAdapter profile_id（须已注册，如 stub_engine）",
    )
    ap.add_argument(
        "--spec",
        type=str,
        default="",
        help="spec.json 路径（与 --intake 二选一）",
    )
    ap.add_argument(
        "--intake",
        type=str,
        default="",
        help="真源 intake（json；csv/xlsx 桩）",
    )
    ap.add_argument(
        "--write-spec",
        action="store_true",
        help="intake 后将 spec 写盘到 --spec-out",
    )
    ap.add_argument(
        "--spec-out",
        type=str,
        default="",
        help="--write-spec 目标路径（必填当 --write-spec）",
    )
    ap.add_argument(
        "--host-package",
        action="append",
        default=[],
        metavar="PKG",
        help="宿主 Python 包名，import 后注册 EngineAdapter（可重复）。"
        "亦可用环境变量 FIGHT_ENTITY_HOST_PACKAGES（分号/逗号分隔）",
    )
    ap.add_argument(
        "--project-root",
        type=str,
        default="",
        help="宿主项目根目录（默认：CLI 所在目录的上一级）",
    )
    return ap


def run(argv: list[str] | None = None, *, tools_dir: Path | None = None) -> int:
    tools = (tools_dir or Path(__file__).resolve().parent.parent).resolve()
    if str(tools) not in sys.path:
        sys.path.insert(0, str(tools))

    args = build_parser().parse_args(argv)
    root = Path(args.project_root).resolve() if args.project_root else project_root(tools)
    eid = int(args.entity_id)
    profile = (args.profile or "").strip()

    host_pkgs = packages_from_env() + list(args.host_package or [])
    if host_pkgs:
        loaded = register_host_packages(host_pkgs)
        print(f"[host] registered packages: {', '.join(loaded)}")

    if args.intake:
        spec = intake_to_spec(
            Path(args.intake),
            eid,
            pipeline_profile=profile or "stub_engine",
        )
        if args.write_spec:
            if not args.spec_out:
                print("[error] --write-spec 须同时指定 --spec-out", file=sys.stderr)
                return 1
            sp_out = Path(args.spec_out).resolve()
            sp_out.parent.mkdir(parents=True, exist_ok=True)
            sp_out.write_text(
                json.dumps(spec, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
            print(f"[ok] spec written: {sp_out}")
    elif args.spec:
        sp = Path(args.spec).resolve()
        if not sp.is_file():
            print(f"[error] spec not found: {sp}", file=sys.stderr)
            return 1
        spec = load_spec(sp, eid)
    else:
        print("[error] 须指定 --spec 或 --intake", file=sys.stderr)
        return 1

    profile = profile or str(spec.get("pipeline_profile") or "stub_engine")
    try:
        adapter = get_adapter(profile, root)
    except KeyError as exc:
        print(f"[error] {exc}", file=sys.stderr)
        return 1

    print(
        f"[pipeline] profile={profile} adapter={adapter.__class__.__name__} entity_id={eid}"
    )

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
