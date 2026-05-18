import argparse
import json
import random
import sys
from datetime import datetime, timezone
from pathlib import Path

from ones.storage.paths import require_character_dir

hour = datetime.now().hour

if 5 <= hour < 11:
    time_of_day = "morning"
elif 11 <= hour < 17:
    time_of_day = "day"
elif 17 <= hour < 22:
    time_of_day = "evening"
else:
    time_of_day = "night"

sys.path.append(str(Path(__file__).resolve().parents[1]))


def now_iso():
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--one", required=True)
    args = parser.parse_args()

    base = require_character_dir(args.one)
    body_path = base / "body" / "state.json"

    summary = random.choice(
        [
            "近くに人の気配がある",
            "部屋は静か",
            "少しあたたかい",
            "机の上でじっとしている",
            "周囲に大きな変化はない",
        ]
    )

    human_nearby = "人の気配" in summary

    body = {
        "body_type": "mock",
        "location": random.choice(["desk", "room", "unknown"]),
        "battery": random.randint(40, 100),
        "temperature": round(random.uniform(24.0, 38.0), 1),
        "human_nearby": human_nearby,
        "time_of_day": time_of_day,
        "sensor_summary": summary,
        "updated_at": now_iso(),
    }

    body_path.write_text(json.dumps(body, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"updated mock body: {args.one}")


if __name__ == "__main__":
    main()
