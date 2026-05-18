from pathlib import Path

import yaml


def read_yaml(path: Path) -> dict:
    if not path.exists() or path.read_text(encoding="utf-8").strip() == "":
        return {}

    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}
