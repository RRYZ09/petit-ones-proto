import json
import urllib.parse
import urllib.request
from urllib.error import HTTPError, URLError

from ones.storage.paths import require_character_dir
from ones.utils.json_file import write_json
from ones.utils.time import now_iso
from ones.utils.yaml_file import read_yaml


def fetch_json(url: str, timeout_sec: float) -> dict:
    with urllib.request.urlopen(url, timeout=timeout_sec) as response:
        body = response.read().decode("utf-8", errors="replace")
        return json.loads(body)


def fetch_text(url: str, timeout_sec: float) -> str:
    with urllib.request.urlopen(url, timeout=timeout_sec) as response:
        return response.read().decode("utf-8", errors="replace")


def resolve_base_url(base_urls: list[str], timeout_sec: float) -> str:
    last_error = None

    for base_url in base_urls:
        base_url = base_url.rstrip("/")
        try:
            fetch_json(f"{base_url}/status", timeout_sec)
            return base_url
        except (URLError, HTTPError, TimeoutError, OSError, json.JSONDecodeError) as exc:
            last_error = exc

    raise RuntimeError(f"No reachable M5 CoreS3 endpoint. Last error: {last_error}")


def get_m5_cores3_config(one_id: str) -> tuple[dict, str, float]:
    base = require_character_dir(one_id)
    config = read_yaml(base / "config" / "body.yaml")

    m5 = config.get("m5_cores3", {})
    base_urls = m5.get("base_urls", [])
    timeout_sec = float(m5.get("timeout_sec", 1.5))

    if not base_urls:
        base_url = m5.get("base_url")
        if base_url:
            base_urls = [base_url]

    if not base_urls:
        raise ValueError("Missing m5_cores3.base_urls in config/body.yaml")

    base_url = resolve_base_url(base_urls, timeout_sec)
    return m5, base_url, timeout_sec


def summarize_sensors(sensors: dict, status: dict) -> str:
    parts = []

    if status.get("is_sleeping") is True:
        parts.append("眠っている")
    else:
        parts.append("起きている")

    proximity = sensors.get("proximity")
    if isinstance(proximity, (int, float)):
        if proximity > 1000:
            parts.append("近くに何かがある")
        else:
            parts.append("近くに大きな反応はない")

    ambient = sensors.get("ambient")
    if isinstance(ambient, (int, float)):
        if ambient < 50:
            parts.append("周囲は暗い")
        elif ambient > 1000:
            parts.append("周囲は明るい")

    battery = sensors.get("battery")
    if isinstance(battery, (int, float)):
        parts.append(f"バッテリーは{battery:.0f}%")

    return "、".join(parts)


def update_m5_cores3_body(one_id: str) -> dict:
    base = require_character_dir(one_id)
    m5, base_url, timeout_sec = get_m5_cores3_config(one_id)

    status = fetch_json(f"{base_url}/status", timeout_sec)
    sensors = fetch_json(f"{base_url}/sensors", timeout_sec)

    proximity = sensors.get("proximity")
    human_nearby = isinstance(proximity, (int, float)) and proximity > 1000

    body = {
        "body_type": "m5_cores3",
        "location": m5.get("location", "desk"),
        "battery": sensors.get("battery"),
        "temperature": None,
        "human_nearby": human_nearby,
        "sensor_summary": summarize_sensors(sensors, status),
        "time_of_day": None,
        "m5_cores3": {
            "base_url": base_url,
            "is_sleeping": status.get("is_sleeping"),
            "power_save": status.get("power_save"),
            "ambient": sensors.get("ambient"),
            "proximity": sensors.get("proximity"),
            "voltage": sensors.get("voltage"),
            "rssi": sensors.get("rssi"),
            "accel": {
                "x": sensors.get("ax"),
                "y": sensors.get("ay"),
                "z": sensors.get("az"),
            },
            "gyro": {
                "x": sensors.get("gx"),
                "y": sensors.get("gy"),
                "z": sensors.get("gz"),
            },
            "last_touch_event_time": sensors.get("lastTouchEventTime"),
        },
        "updated_at": now_iso(),
    }

    write_json(base / "body" / "state.json", body)
    return body


def set_face(one_id: str, eye_x: int = 0, eye_y: int = 0, mouth: int = 0) -> None:
    _, base_url, timeout_sec = get_m5_cores3_config(one_id)

    query = urllib.parse.urlencode(
        {
            "eyeX": eye_x,
            "eyeY": eye_y,
            "mouth": mouth,
        }
    )
    fetch_text(f"{base_url}/set_face_draw?{query}", timeout_sec)


def blink(one_id: str, left: bool = True, right: bool = True) -> None:
    _, base_url, timeout_sec = get_m5_cores3_config(one_id)

    query = urllib.parse.urlencode(
        {
            "left": str(left).lower(),
            "right": str(right).lower(),
        }
    )
    fetch_text(f"{base_url}/blink?{query}", timeout_sec)
