import argparse
import json
import os

import requests
from dotenv import load_dotenv

load_dotenv(".env")

TYPETALK_URL = os.environ.get("TYPETALK_URL")
TYPETALK_TOKEN = os.environ.get("TYPETALK_TOKEN")
SLACK_URL = os.environ.get("SLACK_URL")


def parse_args():
    parser = argparse.ArgumentParser(description="")
    parser.add_argument(
        "--message",
        type=str,
        default="test",
        help="message for sending SNS",
    )
    args = parser.parse_args()
    return args


def send_slack(message: str, url: str) -> None:
    requests.post(
        url,
        data=json.dumps(
            {
                "text": message,
            }
        ),
    )


def send_typetalk(message: str, url: str, token: str) -> None:
    data = {"message": message}
    headers = {"X-TYPETALK-TOKEN": token}
    req = requests.post(url, json=data, headers=headers)
    print(req.status_code)
    print(req.json())


def send_message(args) -> None:
    send_typetalk(args.message, TYPETALK_URL, TYPETALK_TOKEN)
    send_slack(args.message, SLACK_URL)


def main():
    args = parse_args()
    send_message(args)


if __name__ == "__main__":
    main()
