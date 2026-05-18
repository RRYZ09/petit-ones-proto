import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from ones.memory.sqlite_memory import SQLiteMemory
from ones.storage.paths import require_character_dir

sys.path.append(str(Path(__file__).resolve().parents[1]))


def update_desire_after_action(desire: dict, action: str) -> dict:
    updated = dict(desire)

    def clamp(x):
        return max(0.0, min(1.0, round(x, 3)))

    if action == "observe_world":
        updated["curiosity"] = clamp(updated.get("curiosity", 0) - 0.12)
        updated["expression"] = clamp(updated.get("expression", 0) + 0.05)

    elif action == "express_feeling":
        updated["expression"] = clamp(updated.get("expression", 0) - 0.12)
        updated["connection"] = clamp(updated.get("connection", 0) + 0.04)

    elif action == "look_for_human":
        updated["connection"] = clamp(updated.get("connection", 0) - 0.10)
        updated["rest"] = clamp(updated.get("rest", 0) + 0.03)

    elif action == "rest":
        updated["rest"] = clamp(updated.get("rest", 0) - 0.15)
        updated["curiosity"] = clamp(updated.get("curiosity", 0) + 0.03)

    updated["updated_at"] = now_iso()
    return updated


def now_iso():
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def read_json(path: Path) -> dict:
    if not path.exists() or path.read_text(encoding="utf-8").strip() == "":
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def memory_text_for_action(one_id: str, action: str) -> str:
    if action == "observe_world":
        return f"{one_id}は世界を観察した。"
    if action == "express_feeling":
        return f"{one_id}は感じたことを表そうとした。"
    if action == "look_for_human":
        return f"{one_id}は人の気配を探した。"
    if action == "rest":
        return f"{one_id}は少し休んだ。"
    return f"{one_id}はその場にいた。"


def choose_action(desire: dict, body: dict, last_action: str | None = None) -> str:
    scores = {k: v for k, v in desire.items() if isinstance(v, (int, float))}

    if not scores:
        return "stay_still"

    action_map = {
        "curiosity": "observe_world",
        "expression": "express_feeling",
        "connection": "look_for_human",
        "rest": "rest",
    }

    action_scores = {action_map[k]: v for k, v in scores.items() if k in action_map}

    if last_action in action_scores:
        action_scores[last_action] *= 0.7

    return max(action_scores, key=action_scores.get)


def reason_for_action(action: str, desire: dict, recent_memories: list) -> str:
    memory_count = len(recent_memories)

    if action == "observe_world":
        return f"好奇心が一番強かったので、世界を観察することにした。最近の記憶は{memory_count}件ある。"
    if action == "express_feeling":
        return f"表現したい気持ちが強くなっていたので、感じたことを表そうとした。最近の記憶は{memory_count}件ある。"
    if action == "look_for_human":
        return f"関わりたい気持ちが残っていたので、人の気配を探した。最近の記憶は{memory_count}件ある。"
    if action == "rest":
        return (
            f"休みたい気持ちが強かったので、少し休むことにした。最近の記憶は{memory_count}件ある。"
        )

    return f"大きく動かず、その場にいることにした。最近の記憶は{memory_count}件ある。"


def mood_from_state(desire: dict, body: dict) -> str:
    rest = desire.get("rest", 0)
    connection = desire.get("connection", 0)
    curiosity = desire.get("curiosity", 0)

    battery = body.get("battery")

    if isinstance(battery, (int, float)) and battery <= 30:
        return "tired"

    if rest >= 0.6:
        return "sleepy"

    if connection >= 0.5:
        return "social"

    if curiosity >= 0.5:
        return "curious"

    return "calm"


def apply_body_to_desire(desire: dict, body: dict) -> tuple[dict, list[str]]:
    updated = dict(desire)
    effects = []

    def clamp(x):
        return max(0.0, min(1.0, round(x, 3)))

    if body.get("human_nearby") is True:
        updated["connection"] = clamp(updated.get("connection", 0) + 0.08)
        effects.append("人の気配があったので connection が上がった")

    temperature = body.get("temperature")
    if isinstance(temperature, (int, float)) and temperature >= 34.0:
        updated["rest"] = clamp(updated.get("rest", 0) + 0.08)
        effects.append("温度が高かったので rest が上がった")

    battery = body.get("battery")
    if isinstance(battery, (int, float)) and battery <= 50:
        updated["rest"] = clamp(updated.get("rest", 0) + 0.06)
        effects.append("バッテリーが少なかったので rest が上がった")

    sensor_summary = body.get("sensor_summary", "")
    if "変化" in sensor_summary or "人の気配" in sensor_summary:
        updated["curiosity"] = clamp(updated.get("curiosity", 0) + 0.05)
        effects.append("周囲に変化があったので curiosity が上がった")

    if body.get("time_of_day") == "night":
        updated["rest"] = clamp(updated.get("rest", 0) + 0.05)
        effects.append("夜なので rest が上がった")

    if body.get("time_of_day") == "morning":
        updated["curiosity"] = clamp(updated.get("curiosity", 0) + 0.04)
        effects.append("朝なので curiosity が上がった")

    updated["updated_at"] = now_iso()
    return updated, effects


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--one", required=True)
    args = parser.parse_args()

    base = require_character_dir(args.one)

    state_path = base / "state.json"
    desire_path = base / "desire" / "state.json"
    body_path = base / "body" / "state.json"
    action_log_path = base / "logs" / "actions.log"

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

    action_log_path.parent.mkdir(parents=True, exist_ok=True)
    thought_log_path = base / "logs" / "thoughts.log"
    action_log_path.open("a", encoding="utf-8").write(
        json.dumps(
            {
                "time": timestamp,
                "one_id": args.one,
                "action": action,
                "desire": desire,
                "body": body,
                "body_effects": body_effects,
            },
            ensure_ascii=False,
        )
        + "\n"
    )
    thought_log_path.open("a", encoding="utf-8").write(
        json.dumps(
            {
                "time": timestamp,
                "one_id": args.one,
                "action": action,
                "reason": reason,
                "recent_memories": recent_memories,
                "body_effects": body_effects,
                "mood": state["mood"],
            },
            ensure_ascii=False,
        )
        + "\n"
    )

    print(f"{args.one} chose action: {action}")

    memory.add(
        one_id=args.one,
        kind="action",
        content=memory_text_for_action(args.one, action),
        source="run_once",
    )


if __name__ == "__main__":
    main()
