# 在新项目基于框架搭建定制 Agent

## 1. 引入框架仓

```bash
git submodule add <framework-repo-url> vendor/fight-entity-agent-framework
```

或拷贝 `export_framework_repo.ps1` 产出目录。

将 `vendor/fight-entity-agent-framework/cursor/` 链到项目 `.cursor/`（复制或 junction），或把该路径加入 Cursor 多根工作区。

## 2. 注册 EngineAdapter

1. 新建 `tools/fight_entity_host_<project>/`（**宿主包，不进框架仓**）
2. 复制 `templates/EngineAdapter.py.template` → `fight_entity_host_<project>/<engine>_adapter.py`
3. 实现六个钩子，`profile_id = "<your_project>_engine"`，用 `@register_adapter` 装饰
4. 在 `__init__.py` 中 `import` adapter；宿主 `run_fight_entity_pipeline` 包装脚本里 `import fight_entity_host_<project>`

## 3. 新增项目 Agent 层（不进框架仓）

| 文件 | 作用 |
| --- | --- |
| `.cursor/rules/<project>-agent-profile.mdc` | 引擎名、路径、表真源、禁止项 |
| `.cursor/skills/<project>-orchestrator-doc/SKILL.md` | Phase 写集、验收、参考实体 |
| `.cursor/commands/战斗管线-<项目>.md` | Slash 入口（可选） |

从 `templates/project-agent-profile.mdc.template` 生成。

## 4. 配置真源 Intake

扩展 `fight_entity_core/intake.py` 或在项目仓写 `tools/<project>_intake.py`，输出符合 `spec.schema.json` 的 JSON。

Excel / DataTable / JSON 三种入口归一为 **同一 spec**，Agent 主链不变。

## 5. 验证

```bash
python vendor/.../run_fight_entity_pipeline.py --entity-id <id> --profile <your_project>_engine --intake <spec.json>
```

stdout 须出现 `[pipeline-ledger] converged=true`。

## 6. 望月作为参考宿主

望月 `tools/fight_entity_host_wangyue/` 是 **宿主实现示例**，放在游戏仓，不进入框架 Git。
