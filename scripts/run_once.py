import argparse

from ones.core.lifecycle import run_once


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--one", required=True)
    args = parser.parse_args()

    action = run_once(args.one)
    print(f"{args.one} chose action: {action}")


if __name__ == "__main__":
    main()
