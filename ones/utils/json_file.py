import json
from pathlib import Path


def read_json(path: Path) -> dict:
    if not path.exists() or path.read_text(encoding="utf-8").strip() == "":
        return {}

    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
