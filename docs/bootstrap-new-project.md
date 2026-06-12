# 在新项目基于框架搭建定制 Agent

## 1. 引入框架仓

```bash
git submodule add https://github.com/myrainbowcolor/Game-Agent.git vendor/Game-Agent
```

将 `vendor/Game-Agent/cursor/` 链到项目 `.cursor/`（复制、junction 或多根工作区）。

## 2. 注册 EngineAdapter

1. 新建 `tools/fight_entity_host_<project>/`（**宿主包，不进框架仓**）
2. 复制 `templates/EngineAdapter.py.template` → `fight_entity_host_<project>/<engine>_adapter.py`
3. 实现六个钩子，`profile_id = "<your_project>_engine"`，用 `@register_adapter` 装饰
4. 在 `__init__.py` 中 `import` adapter；复制 `templates/host-run-cli.py.template` 为项目 `run_pipeline.py`，注入 `--host-package`

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
python vendor/Game-Agent/python/run_fight_entity_pipeline.py \
  --host-package fight_entity_host_<project> \
  --entity-id <id> --profile <your_project>_engine --intake <spec.json>
```

stdout 须出现 `[pipeline-ledger] converged=true`。
