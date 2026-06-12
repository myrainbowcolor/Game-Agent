---
name: wy-fight-entity-core-doc
description: 引擎无关战斗实体管线：spec 契约、EngineAdapter、intake、run_fight_entity_pipeline、打包组件划分。自研/多引擎复用 Agent 时先读本 Skill。
---

# Fight Entity Core（引擎无关）

## 何时用

- 目标引擎**自研**或**非望月 Unity**
- 配置真源可能是 **Excel / DataTable / JSON**
- 需要把 **Agent 编排 + 打包 zip** 迁到新项目，但不搬 Unity 写盘链

望月 Unity 满月灵接入仍用 `wy-fight-entity-orchestrator-doc` + `run_yueling_battle_pipeline_from_spec.py`。

## 架构

```text
Intake (xlsx|csv|json) → spec.json → EngineAdapter(profile) → Phase 链 → P-VERIFY
```

| 文件 | 作用 |
| --- | --- |
| `tools/fight_entity_core/spec.schema.json` | spec v0 schema |
| `tools/fight_entity_core/adapter.py` | `EngineAdapter` 六个钩子 |
| `tools/fight_entity_core/intake.py` | 真源 → spec（表类现为桩） |
| `tools/fight_entity_core/adapters/stub_engine.py` | 自研占位实现 |
| `tools/fight_entity_host_wangyue/` | 望月宿主 adapter（**游戏仓**，非框架 Git） |
| `tools/run_fight_entity_pipeline.py` | 统一 CLI |

## CLI

```bash
# 桩引擎（验证编排）
python tools/run_fight_entity_pipeline.py --entity-id 9000001 --profile stub_engine --intake path/to/spec.json --write-spec

# 望月 Unity（委托旧管线）
python tools/run_fight_entity_pipeline.py --entity-id 6010300 --profile unity_wangyue
```

## 新引擎接入清单

1. 新建 `fight_entity_core/adapters/<your_engine>.py`，`profile_id = "custom_engine_v1"`
2. 实现：`preflight_logic_asset` / `generate_main_entity` / `generate_derived` / `wire_skills` / `export_runtime` / `verify`
3. 在 `adapters/__init__.py` import 注册
4. 扩展 `intake.py` 映射 Excel/DataTable
5. 可选：`.cursor/rules` 增加 `<engine>-profile.mdc`（引擎专用，不放进 core 包）

## 独立 Git 框架仓

跨项目通用内容用 **`tools/fight_entity_agent_framework/export_framework_repo.ps1`** 导出为独立仓库。

| 进框架 Git | 留宿主项目 Git |
| --- | --- |
| `fight_entity_core`（仅 stub adapter） | `fight_entity_host_<project>/` |
| `fight-entity-core-portable.mdc` + 本 Skill | `link-to-fight-entity-*`、`yueling_*` |
| `spec.schema.json`、模板 | Excel 映射、strict_gate 具体项 |

详见 `tools/fight_entity_agent_framework/docs/git-split-boundary.md`。

## Phase（与望月对照）

| Core Phase | EngineAdapter 方法 |
| --- | --- |
| P-PREFAB | `preflight_logic_asset` |
| P-ENTITY | `generate_main_entity` |
| P-DERIVED-ENTITY | `generate_derived` |
| P-SKILL | `wire_skills` |
| P-EXPORT | `export_runtime` |
| P-VERIFY | `verify` |

## 维护

- 打包清单：`tools/fight_entity_pipeline_bundle_manifest.json`
- 分发说明：`docs/knowledge/references/fight-entity-pipeline-distribution-pack.md`
