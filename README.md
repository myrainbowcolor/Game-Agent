# Game-Agent

跨项目、引擎无关的**游戏配置生产 Agent 框架**。

- **仓库**：https://github.com/myrainbowcolor/Game-Agent
- **当前模块**：战斗实体 `fight_entity_core`（v0.2.0）

## 设计原则

**框架层零宿主硬编码**：不含任何具体游戏项目包名、默认表路径、实体号段。  
宿主通过 `fight_entity_host_<project>/` + `--host-package` 接入。

## 目录

```text
Game-Agent/
├── python/fight_entity_core/       # 内核 + stub adapter + host_loader
├── python/run_fight_entity_pipeline.py
├── schema/spec.schema.json
├── cursor/rules/fight-entity-core-portable.mdc
├── cursor/skills/game-agent-fight-entity-core/
├── templates/
└── docs/
```

## 快速开始

```bash
git submodule add https://github.com/myrainbowcolor/Game-Agent.git vendor/Game-Agent
```

```bash
python vendor/Game-Agent/python/run_fight_entity_pipeline.py \
  --entity-id 9000001 \
  --profile stub_engine \
  --intake path/to/spec.json
```

stdout 须出现 `[pipeline-ledger] converged=true`。

## 宿主接入

见 [docs/bootstrap-new-project.md](docs/bootstrap-new-project.md)。

1. 实现 `fight_entity_host_<project>/` 并 `@register_adapter`
2. 用 `templates/host-run-cli.py.template` 生成项目 `run_pipeline.py`
3. 在项目仓写 Agent profile 与 orchestrator Skill

## 框架 vs 宿主

| 框架 Git（本仓） | 宿主项目 Git |
| --- | --- |
| spec schema、EngineAdapter 契约 | 表列映射、引擎写盘 |
| stub_engine、CLI、host_loader | `fight_entity_host_<project>/` |
| 通用 Cursor rules/skills | 项目 profile、验收细则 |

详见 [docs/git-split-boundary.md](docs/git-split-boundary.md)。

## 维护者同步

框架开发真源在内部 monorepo 的 `client/tools/fight_entity_core/`；发版用 `export_framework_repo.ps1`（路径见各宿主项目文档，**不随本仓分发**）。
