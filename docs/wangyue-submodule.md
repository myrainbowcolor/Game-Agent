# 望月 client 引用 Game-Agent

## Submodule（推荐）

在 `wangyue/client` 根目录：

```bash
git submodule add https://github.com/myrainbowcolor/Game-Agent.git vendor/Game-Agent
git submodule update --init --recursive
```

## Python 路径

将 `vendor/Game-Agent/python` 加入 `PYTHONPATH`，或在宿主包装脚本中：

```python
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "vendor" / "Game-Agent" / "python"))
```

## Cursor

- 框架规则：`vendor/Game-Agent/cursor/rules/fight-entity-core-portable.mdc`
- 框架 Skill：`vendor/Game-Agent/cursor/skills/wy-fight-entity-core-doc/`
- 望月专用：保留在 `client/.cursor/`（`link-to-fight-entity-*` 等）

Agent 顺序：**先读 Game-Agent 框架 Skill → 再读望月 profile**。

## 望月宿主包（不进 Game-Agent）

`client/tools/fight_entity_host_wangyue/` 委托 `run_yueling_battle_pipeline_from_spec.py`。

开发真源仍在望月 `tools/fight_entity_core/`；发版时用 `export_framework_repo.ps1` 同步到 Game-Agent。
