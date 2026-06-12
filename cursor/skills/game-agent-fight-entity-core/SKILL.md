---
name: game-agent-fight-entity-core
description: Game-Agent 战斗实体框架：spec 契约、EngineAdapter、host 注册、run_fight_entity_pipeline。跨项目 Agent 先读本 Skill。
---

# Game-Agent · Fight Entity Core

## 何时用

- 任意游戏项目基于 [Game-Agent](https://github.com/myrainbowcolor/Game-Agent) 搭建配置 Agent
- 配置真源为 Excel / DataTable / JSON，需归一为 **spec.json**
- 需要引擎无关 Phase 链与 `[pipeline-ledger]` 收口

## 架构

```text
Intake → spec.json → EngineAdapter(profile) → Phase 链 → P-VERIFY
```

| 组件 | 路径（框架仓） |
| --- | --- |
| spec schema | `schema/spec.schema.json` |
| 内核 | `python/fight_entity_core/` |
| stub adapter | `python/fight_entity_core/adapters/stub_engine.py` |
| CLI | `python/run_fight_entity_pipeline.py` |
| host 注册 | `python/fight_entity_core/host_loader.py` |

## CLI（框架层，零宿主硬编码）

```bash
python vendor/Game-Agent/python/run_fight_entity_pipeline.py \
  --entity-id 9000001 \
  --profile stub_engine \
  --intake path/to/spec.json
```

注册宿主 adapter：

```bash
python vendor/Game-Agent/python/run_fight_entity_pipeline.py \
  --host-package fight_entity_host_mygame \
  --entity-id 1001 --profile mygame_engine --spec path/to/spec.json
```

或 `FIGHT_ENTITY_HOST_PACKAGES=fight_entity_host_mygame`。

**须**提供 `--spec` 或 `--intake`；`--write-spec` 须配 `--spec-out`。

## 宿主项目清单

1. `tools/fight_entity_host_<project>/` + `@register_adapter`
2. 可选 `run_pipeline.py` 包装：注入 `--host-package` 与项目默认 spec 路径
3. `.cursor/rules/<project>-agent-profile.mdc` + orchestrator Skill（不进框架仓）
4. 扩展 intake 映射到 `spec.schema.json`

## Phase

| Phase | EngineAdapter 方法 |
| --- | --- |
| P-PREFAB | `preflight_logic_asset` |
| P-ENTITY | `generate_main_entity` |
| P-DERIVED-ENTITY | `generate_derived` |
| P-SKILL | `wire_skills` |
| P-EXPORT | `export_runtime` |
| P-VERIFY | `verify` |

## 维护

- 边界：`docs/git-split-boundary.md`
- 宿主接入：`docs/bootstrap-new-project.md`
