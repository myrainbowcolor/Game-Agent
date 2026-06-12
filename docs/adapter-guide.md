# EngineAdapter 实现指南

## 接口（框架仓 `fight_entity_core/adapter.py`）

| 方法 | Phase | 职责 |
| --- | --- | --- |
| `preflight_logic_asset` | P-PREFAB | 逻辑资源预检/生成 |
| `generate_main_entity` | P-ENTITY | 主实体配置落盘 |
| `generate_derived` | P-DERIVED-ENTITY | 派生体 |
| `wire_skills` | P-SKILL | 技能与效果衔接 |
| `export_runtime` | P-EXPORT | 导表/运行时导出 |
| `verify` | P-VERIFY | 终局门禁 |

返回 `PhaseResult(phase_id, exit_code, write_set, messages, gaps)`。

## 表写入（Excel / DataTable / JSON）

不要为每种表格式写一条 Agent 管线。在 spec 里用 `table_patches[]`：

```json
{
  "target": "monster_attr",
  "format": "datatable",
  "asset": "/Game/Data/DT_Monster",
  "row_key": 9000001,
  "columns": { "hp": 1000 }
}
```

在 `export_runtime` 内按 `format` 分发 writer（项目仓实现）。

## 注册

```python
from fight_entity_core.adapter import EngineAdapter, PhaseResult, register_adapter

@register_adapter
class MyEngineAdapter(EngineAdapter):
    profile_id = "my_engine_v1"
    ...
```

## 参考

- 桩：`adapters/stub_engine.py`（框架仓）
- 宿主委托：项目仓 `fight_entity_host_<project>/`（可包装既有管线脚本，不进框架仓）
