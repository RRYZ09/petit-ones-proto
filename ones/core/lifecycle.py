from ones.body.expression import express_action
from ones.core.action import choose_action
from ones.core.logging import append_jsonl
from ones.core.memory_text import memory_text_for_action
from ones.core.mood import mood_from_state
from ones.core.reason import reason_for_action
from ones.desire.engine import apply_body_to_desire, update_desire_after_action
from ones.memory.legacy_memory import LegacyMemory
from ones.memory.sqlite_memory import SQLiteMemory
from ones.storage.paths import require_character_dir
from ones.utils.json_file import read_json, write_json
from ones.utils.time import now_iso
from ones.utils.yaml_file import read_yaml


def ensure_desire_defaults(desire: dict) -> dict:
    defaults = {
        "curiosity": 0.45,
        "expression": 0.35,
        "connection": 0.30,
        "rest": 0.20,
        "updated_at": None,
    }

    return {**defaults, **desire}


def run_once(one_id: str) -> str:
    base = require_character_dir(one_id)
    desire_config = read_yaml(base / "config" / "desire.yaml")

    state_path = base / "state.json"
    desire_path = base / "desire" / "state.json"
    body_path = base / "body" / "state.json"
    action_log_path = base / "logs" / "actions.log"
    thought_log_path = base / "logs" / "thoughts.log"
    legacy_memory_path = base / "legacy" / "memory.db"

    legacy_memories = []

    if legacy_memory_path.exists():
        legacy_memory = LegacyMemory(legacy_memory_path)
        legacy_memories = legacy_memory.important(limit=3)

    state = read_json(state_path)
    desire = read_json(desire_path)
    desire = ensure_desire_defaults(desire)
    body = read_json(body_path)

    desire, body_effects = apply_body_to_desire(desire, body, desire_config)
    write_json(desire_path, desire)

    memory = SQLiteMemory(base / "memory.sqlite3")
    recent_memories = memory.recent(limit=5)

    action = choose_action(desire, body, state.get("last_action"))
    reason = reason_for_action(action, desire, recent_memories + legacy_memories)
    expression_effects = express_action(one_id, body, action)

    desire = update_desire_after_action(desire, action, desire_config)
    write_json(desire_path, desire)

    timestamp = now_iso()

    state["mood"] = mood_from_state(desire, body)
    state["last_action"] = action
    state["updated_at"] = timestamp
    write_json(state_path, state)

    append_jsonl(
        action_log_path,
        {
            "time": timestamp,
            "one_id": one_id,
            "action": action,
            "desire": desire,
            "body": body,
            "body_effects": body_effects,
            "expression_effects": expression_effects,
        },
    )

    append_jsonl(
        thought_log_path,
        {
            "time": timestamp,
            "one_id": one_id,
            "action": action,
            "reason": reason,
            "recent_memories": recent_memories,
            "body_effects": body_effects,
            "mood": state["mood"],
            "expression_effects": expression_effects,
        },
    )

    express_action(one_id, body, action)
    memory.add(
        one_id=one_id,
        kind="action",
        content=memory_text_for_action(one_id, action),
        source="run_once",
    )

    return action
