#!/usr/bin/env python3
"""Game-Agent 框架 CLI 入口（零宿主硬编码）。

宿主项目请自建包装脚本，通过 --host-package 或 FIGHT_ENTITY_HOST_PACKAGES 注册 adapter。

示例:
  python tools/run_fight_entity_pipeline.py --entity-id 9000001 --profile stub_engine --intake path/to/spec.json
  python tools/run_fight_entity_pipeline.py --entity-id 9000001 --profile stub_engine --spec path/to/spec.json
"""
from __future__ import annotations

import sys
from pathlib import Path

_TOOLS = Path(__file__).resolve().parent
if str(_TOOLS) not in sys.path:
    sys.path.insert(0, str(_TOOLS))

from fight_entity_core.cli import run


def main() -> int:
    return run(tools_dir=_TOOLS)


if __name__ == "__main__":
    raise SystemExit(main())
