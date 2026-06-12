# Fight Entity Agent Framework

跨项目、引擎无关的战斗实体配置 **Agent 框架**（非完整游戏管线）。

## 框架提供

- **spec.schema.json**：策划真源归一化后的中间契约
- **EngineAdapter**：六个 Phase 钩子（P-PREFAB … P-VERIFY）
- **run_fight_entity_pipeline.py**：CLI 驱动
- **Cursor**：`fight-entity-core-portable.mdc` + `game-agent-fight-entity-core`

## 框架不提供

- Unity / UE / 自研引擎的写盘与编辑器 API
- 具体游戏 Excel 表结构、实体 JSON schema
- 具体游戏表结构、实体 JSON、引擎编辑器 API

上述由**宿主项目** `fight_entity_host_<project>/` + 项目 rules/skills 实现。

## 目录（独立 Git 仓）

```
fight-entity-agent-framework/
├── python/fight_entity_core/
├── python/run_fight_entity_pipeline.py
├── schema/spec.schema.json
├── cursor/rules/
├── cursor/skills/
├── templates/
└── docs/
```

## 宿主项目接入

见 `docs/bootstrap-new-project.md`。

## 远程仓

https://github.com/myrainbowcolor/Game-Agent

各宿主项目维护者从内部 monorepo 同步 `fight_entity_core` 后 push 本仓（框架层零宿主硬编码）。
