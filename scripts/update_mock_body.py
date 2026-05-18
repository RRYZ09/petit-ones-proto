import argparse

from ones.body.mock_body import update_mock_body


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--one", required=True)
    args = parser.parse_args()

    update_mock_body(args.one)
    print(f"updated mock body: {args.one}")


if __name__ == "__main__":
    main()
