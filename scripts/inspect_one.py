import argparse
import json
import sys
from pathlib import Path

from ones.storage.paths import require_character_dir

sys.path.append(str(Path(__file__).resolve().parents[1]))


def read_text_if_exists(path: Path) -> str:
    if not path.exists():
        return "(missing)"
    return path.read_text(encoding="utf-8").strip()


def read_json_if_exists(path: Path):
    if not path.exists():
        return "(missing)"
    if path.read_text(encoding="utf-8").strip() == "":
        return "(empty)"
    return json.loads(path.read_text(encoding="utf-8"))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--one", required=True)
    args = parser.parse_args()

    base = require_character_dir(args.one)

    print(f"one: {args.one}")
    print(f"path: {base}")
    print()

    print("== SOUL.md ==")
    print(read_text_if_exists(base / "SOUL.md"))
    print()

    print("== state.json ==")
    print(read_json_if_exists(base / "state.json"))
    print()

    print("== desire/state.json ==")
    print(read_json_if_exists(base / "desire" / "state.json"))
    print()

    print("== body/state.json ==")
    print(read_json_if_exists(base / "body" / "state.json"))
    print()

    print("== memory.sqlite3 ==")
    print(base / "memory.sqlite3")


if __name__ == "__main__":
    main()
