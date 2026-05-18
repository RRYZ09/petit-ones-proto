import argparse
import sys
from pathlib import Path

from ones.memory.sqlite_memory import SQLiteMemory
from ones.storage.paths import require_character_dir

sys.path.append(str(Path(__file__).resolve().parents[1]))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--one", required=True)
    parser.add_argument("--limit", type=int, default=10)
    args = parser.parse_args()

    base = require_character_dir(args.one)
    memory = SQLiteMemory(base / "memory.sqlite3")

    for item in memory.recent(args.limit):
        print(f"[{item['created_at']}] {item['kind']} {item['content']}")


if __name__ == "__main__":
    main()
