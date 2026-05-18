import argparse

from ones.memory.legacy_memory import LegacyMemory
from ones.storage.paths import require_character_dir


def print_memory(item: dict) -> None:
    # print(
    #     f"[{item['created_at']}] {item['kind']} /
    # emotion={item['emotion']} / importance={item['importance']}"
    # )
    print(item["content"])
    if item.get("tags"):
        print(f"tags: {item['tags']}")
    if item.get("episode_id"):
        print(f"episode_id: {item['episode_id']}")
    print()


def print_episode(item: dict) -> None:
    print(f"[{item['created_at']}] episode / importance={item['importance']}")
    print(f"title: {item['title']}")
    print(item["summary"])
    print()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--one", required=True)
    parser.add_argument("--limit", type=int, default=5)
    parser.add_argument(
        "--mode",
        choices=["recent", "important", "episodes", "search"],
        default="recent",
    )
    parser.add_argument("--query", default="")
    args = parser.parse_args()

    base = require_character_dir(args.one)
    memory = LegacyMemory(base / "legacy" / "memory.db")

    if args.mode == "recent":
        for item in memory.recent(args.limit):
            print_memory(item)

    elif args.mode == "important":
        for item in memory.important(args.limit):
            print_memory(item)

    elif args.mode == "episodes":
        for item in memory.episodes(args.limit):
            print_episode(item)

    elif args.mode == "search":
        if not args.query:
            raise ValueError("--query is required when --mode search")

        for item in memory.search(args.query, args.limit):
            print_memory(item)


if __name__ == "__main__":
    main()
