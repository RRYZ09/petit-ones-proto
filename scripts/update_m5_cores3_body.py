import argparse

from ones.body.m5_cores3_body import update_m5_cores3_body


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--one", required=True)
    args = parser.parse_args()

    update_m5_cores3_body(args.one)
    print(f"updated m5 cores3 body: {args.one}")


if __name__ == "__main__":
    main()
