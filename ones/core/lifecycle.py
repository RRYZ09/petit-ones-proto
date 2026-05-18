from ones.core.action import choose_action
from ones.core.logging import append_jsonl
from ones.core.memory_text import memory_text_for_action
from ones.core.mood import mood_from_state
from ones.core.reason import reason_for_action
from ones.desire.engine import apply_body_to_desire, update_desire_after_action
from ones.memory.sqlite_memory import SQLiteMemory
from ones.storage.paths import require_character_dir
from ones.utils.json_file import read_json, write_json
from ones.utils.time import now_iso


def run_once(one_id: str) -> str:
    base = require_character_dir(one_id)

    state_path = base / "state.json"
    desire_path = base / "desire" / "state.json"
    body_path = base / "body" / "state.json"
    action_log_path = base / "logs" / "actions.log"
    thought_log_path = base / "logs" / "thoughts.log"

    state = read_json(state_path)
    desire = read_json(desire_path)
    body = read_json(body_path)

    desire, body_effects = apply_body_to_desire(desire, body)
    write_json(desire_path, desire)

    memory = SQLiteMemory(base / "memory.sqlite3")
    recent_memories = memory.recent(limit=5)

    action = choose_action(desire, body, state.get("last_action"))
    reason = reason_for_action(action, desire, recent_memories)

    desire = update_desire_after_action(desire, action)
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
        },
    )

    memory.add(
        one_id=one_id,
        kind="action",
        content=memory_text_for_action(one_id, action),
        source="run_once",
    )

    return action
