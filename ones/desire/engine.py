from datetime import datetime, timezone


def now_iso() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def clamp(x: float) -> float:
    return max(0.0, min(1.0, round(x, 3)))


def apply_body_to_desire(desire: dict, body: dict) -> tuple[dict, list[str]]:
    updated = dict(desire)
    effects = []

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


def update_desire_after_action(desire: dict, action: str) -> dict:
    updated = dict(desire)

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
