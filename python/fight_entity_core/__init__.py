"""Fight Entity Core — 引擎无关管线内核。"""
from fight_entity_core.adapter import EngineAdapter, PhaseResult, get_adapter, load_spec, register_adapter

__all__ = [
    "EngineAdapter",
    "PhaseResult",
    "get_adapter",
    "load_spec",
    "register_adapter",
]
