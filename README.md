# Game-Agent

跨项目、引擎无关的**游戏配置生产 Agent 框架**（策划真源 → 规范 spec → Phase 管线 → 宿主引擎落盘）。

- **仓库**：https://github.com/myrainbowcolor/Game-Agent
- **当前模块**：战斗实体配置（`fight_entity_core`，v0.1.0）
- **首个宿主参考**：望月 `wangyue/client`（Unity + Excel；宿主代码不进本仓）

## 框架 vs 宿主项目

| 进本仓（Game-Agent） | 留在各游戏项目仓 |
| --- | --- |
| 统一 `spec.schema.json` | Excel/DataTable/JSON 列映射 |
| `EngineAdapter` 契约 + stub | `fight_entity_host_<project>/` 实现 |
| `run_fight_entity_pipeline.py` | 引擎编辑器、导表、运行时 JSON |
| Cursor 通用 rules/skills | 项目 profile、orchestrator、验收细则 |

详见 [docs/git-split-boundary.md](docs/git-split-boundary.md)。

## 目录

```text
Game-Agent/
├── python/fight_entity_core/       # 内核（仅 stub adapter）
├── python/run_fight_entity_pipeline.py
├── schema/spec.schema.json
├── cursor/rules/                   # fight-entity-core-portable.mdc
├── cursor/skills/                  # wy-fight-entity-core-doc
├── templates/                      # 新宿主 adapter / profile 模板
└── docs/                           # 接入与 adapter 指南
```

## 在新项目接入

```bash
git submodule add https://github.com/myrainbowcolor/Game-Agent.git vendor/Game-Agent
```

1. 将 `vendor/Game-Agent/cursor/` 链到项目 `.cursor/`（复制、junction 或多根工作区）
2. 按 [docs/bootstrap-new-project.md](docs/bootstrap-new-project.md) 新建 `fight_entity_host_<project>/`
3. 在项目仓写 `.cursor/rules/<project>-agent-profile.mdc` 与 orchestrator Skill

验证：

```bash
cd <project-root>
python vendor/Game-Agent/python/run_fight_entity_pipeline.py \
  --entity-id <id> --profile stub_engine --intake <spec.json>
```

stdout 须出现 `[pipeline-ledger] converged=true`。

## 从望月开发树同步到本仓

望月 `client/tools/fight_entity_agent_framework/export_framework_repo.ps1` 导出清单见 `REPO_MANIFEST.json`。

维护者在本机：

```powershell
# 在 wangyue/client 下
powershell -ExecutionPolicy Bypass -File tools/fight_entity_agent_framework/export_framework_repo.ps1 -OutputDir <staging>
# 再合并到 Game-Agent 克隆并 push
```

## 模块路线图（规划）

| 模块 | 状态 |
| --- | --- |
| 战斗实体 `fight_entity_core` | v0.1.0 已收录 |
| 关卡 / 任务 / 数值表 Agent | 待扩展（同 spec + adapter 模式） |
