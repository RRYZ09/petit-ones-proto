import random
from datetime import datetime

from ones.storage.paths import require_character_dir
from ones.utils.json_file import write_json
from ones.utils.time import now_iso


def time_of_day_now() -> str:
    hour = datetime.now().hour

    if 5 <= hour < 11:
        return "morning"
    if 11 <= hour < 17:
        return "day"
    if 17 <= hour < 22:
        return "evening"

    return "night"


def generate_mock_body_state() -> dict:
    summary = random.choice(
        [
            "近くに人の気配がある",
            "部屋は静か",
            "少しあたたかい",
            "机の上でじっとしている",
            "周囲に大きな変化はない",
        ]
    )

    return {
        "body_type": "mock",
        "location": random.choice(["desk", "room", "unknown"]),
        "battery": random.randint(40, 100),
        "temperature": round(random.uniform(24.0, 38.0), 1),
        "human_nearby": "人の気配" in summary,
        "sensor_summary": summary,
        "time_of_day": time_of_day_now(),
        "updated_at": now_iso(),
    }


def update_mock_body(one_id: str) -> dict:
    base = require_character_dir(one_id)
    body = generate_mock_body_state()

    write_json(base / "body" / "state.json", body)

    return body
