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
