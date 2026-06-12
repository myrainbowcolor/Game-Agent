# Git 拆分边界：框架仓 vs 宿主项目仓

## 进框架 Git 仓（跨项目通用）

| 类别 | 路径（导出后） |
| --- | --- |
| Python 内核 | `python/fight_entity_core/`、`run_fight_entity_pipeline.py` |
| Spec | `schema/spec.schema.json` |
| Cursor 通用 | `cursor/rules/fight-entity-core-portable.mdc` |
| Cursor Skill | `cursor/skills/game-agent-fight-entity-core/` |
| 文档 | `docs/bootstrap-new-project.md`、`adapter-guide.md`、本文件 |
| 模板 | `templates/*` |

**原则**：框架仓不出现任何具体游戏项目包名、表路径、实体号段、引擎专有 API。

## 留在宿主项目仓（定制化）

| 类别 | 示例 |
| --- | --- |
| EngineAdapter 实现 | `fight_entity_host_<project>/` |
| Intake 映射 | 本项目 Excel/DataTable 列 → spec 字段 |
| 项目 rules | `<project>-agent-profile.mdc` |
| 项目 skills | `<project>-orchestrator-doc`、Phase 细则、验收清单 |
| 项目 tools | 引擎写盘、导表、strict_gate 具体检查项 |
| 编辑器 / 运行时 | 引擎 API、配置导出、运行时加载 |

## Cursor Agent 两层协作

```text
[框架仓] fight-entity-core-portable + game-agent-fight-entity-core
        ↓ spec、Adapter 契约、Phase、ledger、host 注册方式
[项目仓] fight_entity_host_<project> + <project>-agent-profile + orchestrator
        ↓ 表路径、写集、引擎 CLI、默认 spec 路径
```

Agent 在任意项目：**先读框架 Skill，再读项目 profile**；禁止把项目细节写进框架仓。

##  Submodule / 拷贝 建议

| 方式 | 适用 |
| --- | --- |
| **git submodule** `vendor/Game-Agent` | 多项目统一升级框架 |
| **拷贝 + 偶尔 merge** | 单项目强定制 |
| **npm/pip 私有包** | 若只想分发 Python，Cursor 规则仍 submodule |

推荐：框架仓 + 各游戏仓 submodule 引用 `python/` 与 `cursor/`。
