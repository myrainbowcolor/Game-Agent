# Git 拆分边界：框架仓 vs 宿主项目仓

## 进框架 Git 仓（跨项目通用）

| 类别 | 路径（导出后） |
| --- | --- |
| Python 内核 | `python/fight_entity_core/`、`run_fight_entity_pipeline.py` |
| Spec | `schema/spec.schema.json` |
| Cursor 通用 | `cursor/rules/fight-entity-core-portable.mdc` |
| Cursor Skill | `cursor/skills/wy-fight-entity-core-doc/` |
| 文档 | `docs/bootstrap-new-project.md`、`adapter-guide.md`、本文件 |
| 模板 | `templates/*` |

**原则**：仓库内不出现 `EntityNew`、`GenPrefab`、`partner.xlsx`、`6010xxx` 等具体游戏痕迹。

## 留在宿主项目仓（定制化）

| 类别 | 示例（望月） |
| --- | --- |
| EngineAdapter 实现 | `fight_entity_host_wangyue/`、未来 `fight_entity_host_<project>/` |
| Intake 映射 | 本项目 Excel/DataTable 列 → spec 字段 |
| 项目 rules | `link-to-fight-entity-partner-spec.mdc`、`<project>-agent-profile.mdc` |
| 项目 skills | `wy-fight-entity-orchestrator-doc`、Phase 细则、验收清单 |
| 项目 tools | `yueling_*`、`cache_spec_extract`、strict_gate 具体检查项 |
| 编辑器 / 运行时 | Unity C#、导表 bat、Lua 导出 |

## Cursor Agent 两层协作

```text
[框架仓] fight-entity-core-portable + wy-fight-entity-core-doc
        ↓ 只规定：spec、Adapter、Phase、ledger 收口
[项目仓] <project>-agent-profile + <project>-orchestrator-doc
        ↓ 规定：表路径、资源命名、参考实体、引擎 CLI
```

Agent 在任意项目：**先读框架 Skill，再读项目 profile**；禁止把项目细节写进框架仓。

##  Submodule / 拷贝 建议

| 方式 | 适用 |
| --- | --- |
| **git submodule** `vendor/fight-entity-agent-framework` | 多项目统一升级框架 |
| **拷贝 + 偶尔 merge** | 单项目强定制 |
| **npm/pip 私有包** | 若只想分发 Python，Cursor 规则仍 submodule |

推荐：框架仓 + 各游戏仓 submodule 引用 `python/` 与 `cursor/`。
