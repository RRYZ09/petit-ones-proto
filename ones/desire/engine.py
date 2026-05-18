from ones.utils.time import now_iso


def clamp(x: float) -> float:
    return max(0.0, min(1.0, round(x, 3)))


def apply_body_to_desire(
    desire: dict,
    body: dict,
    config: dict | None = None,
) -> tuple[dict, list[str]]:
    updated = dict(desire)
    effects = []

    config = config or {}
    body_effects = config.get("body_effects", {})
    thresholds = config.get("thresholds", {})

    human_nearby_connection = body_effects.get("human_nearby_connection", 0.08)
    high_temperature_rest = body_effects.get("high_temperature_rest", 0.08)
    low_battery_rest = body_effects.get("low_battery_rest", 0.06)
    environmental_change_curiosity = body_effects.get("environmental_change_curiosity", 0.05)
    night_rest = body_effects.get("night_rest", 0.05)
    morning_curiosity = body_effects.get("morning_curiosity", 0.04)

    high_temperature = thresholds.get("high_temperature", 34.0)
    low_battery = thresholds.get("low_battery", 50)

    if body.get("human_nearby") is True:
        updated["connection"] = clamp(updated.get("connection", 0) + human_nearby_connection)
        effects.append("人の気配があったので connection が上がった")

    temperature = body.get("temperature")
    if isinstance(temperature, (int, float)) and temperature >= high_temperature:
        updated["rest"] = clamp(updated.get("rest", 0) + high_temperature_rest)
        effects.append("温度が高かったので rest が上がった")

    battery = body.get("battery")
    if isinstance(battery, (int, float)) and battery <= low_battery:
        updated["rest"] = clamp(updated.get("rest", 0) + low_battery_rest)
        effects.append("バッテリーが少なかったので rest が上がった")

    sensor_summary = body.get("sensor_summary", "")
    if "変化" in sensor_summary or "人の気配" in sensor_summary:
        updated["curiosity"] = clamp(updated.get("curiosity", 0) + environmental_change_curiosity)
        effects.append("周囲に変化があったので curiosity が上がった")

    if body.get("time_of_day") == "night":
        updated["rest"] = clamp(updated.get("rest", 0) + night_rest)
        effects.append("夜なので rest が上がった")

    if body.get("time_of_day") == "morning":
        updated["curiosity"] = clamp(updated.get("curiosity", 0) + morning_curiosity)
        effects.append("朝なので curiosity が上がった")

    updated["updated_at"] = now_iso()
    return updated, effects


def update_desire_after_action(
    desire: dict,
    action: str,
    config: dict | None = None,
) -> dict:
    updated = dict(desire)

    config = config or {}
    action_effects = config.get("action_effects", {})

    default_action_effects = {
        "observe_world": {
            "curiosity": -0.12,
            "expression": 0.05,
        },
        "express_feeling": {
            "expression": -0.12,
            "connection": 0.04,
        },
        "look_for_human": {
            "connection": -0.10,
            "rest": 0.03,
        },
        "rest": {
            "rest": -0.15,
            "curiosity": 0.03,
        },
    }

    effects = action_effects.get(action, default_action_effects.get(action, {}))

    for key, delta in effects.items():
        updated[key] = clamp(updated.get(key, 0) + delta)

    updated["updated_at"] = now_iso()
    return updated
