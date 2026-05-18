import argparse
import random
import time

from ones.body.m5_cores3_body import update_m5_cores3_body
from ones.core.lifecycle import run_once


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--one", required=True)
    args = parser.parse_args()

    while True:
        try:
            update_m5_cores3_body(args.one)
            run_once(args.one)

        except Exception as exc:
            print(f"loop error: {exc}")

        sleep_sec = random.randint(20, 60)
        time.sleep(sleep_sec)


if __name__ == "__main__":
    main()
