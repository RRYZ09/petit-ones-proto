import os
from pathlib import Path


def petit_ones_home() -> Path:
    return Path(os.getenv("PETIT_ONES_HOME", "~/.petit_ones")).expanduser()


def character_dir(one_id: str) -> Path:
    return petit_ones_home() / "characters" / one_id


def require_character_dir(one_id: str) -> Path:
    path = character_dir(one_id)
    if not path.exists():
        raise FileNotFoundError(f"Character not found: {path}")
    return path
