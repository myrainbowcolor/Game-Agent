# Fight Entity Agent Framework

跨项目、引擎无关的战斗实体配置 **Agent 框架**（非完整游戏管线）。

## 框架提供

- **spec.schema.json**：策划真源归一化后的中间契约
- **EngineAdapter**：六个 Phase 钩子（P-PREFAB … P-VERIFY）
- **run_fight_entity_pipeline.py**：CLI 驱动
- **Cursor**：`fight-entity-core-portable.mdc` + `wy-fight-entity-core-doc`

## 框架不提供

- Unity / UE / 自研引擎的写盘与编辑器 API
- 具体游戏 Excel 表结构、实体 JSON schema
- 月灵/望月命名（Mo1F、partner.xlsx 等）

上述由**宿主项目**实现 adapter + 项目 rules/skills。

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

## 开发真源（当前）

望月 `wangyue/client` 内 `tools/fight_entity_core/` 与框架 manifest 同步；  
用 `export_framework_repo.ps1` 导出为独立仓库。
