import argparse
import json
import os

import requests
from dotenv import load_dotenv

load_dotenv(".env")

TYPETALK_URL = os.environ.get("TYPETALK_URL")
TYPETALK_TOKEN = os.environ.get("TYPETALK_TOKEN")
SLACK_URL = os.environ.get("SLACK_URL")

MESSAGE_PATH = "message.txt"


def parse_args():
    parser = argparse.ArgumentParser(description="")
    parser.add_argument(
        "-m",
        "--message",
        type=str,
        default="",
        help="message for sending to SNS",
    )
    parser.add_argument(
        "-s",
        "--sns_type",
        type=str,
        default="slack",
        choices=["typetalk", "slack", "all"],
        help="The name of the SNS.",
    )
    args = parser.parse_args()
    return args


def send_slack(message: str, url: str) -> None:
    request = requests.post(
        url,
        data=json.dumps(
            {
                "text": message,
            }
        ),
    )
    print(f"slack's status code is {request.status_code}.\n")


def send_typetalk(message: str, url: str, token: str) -> None:
    data = {"message": message}
    headers = {"X-TYPETALK-TOKEN": token}
    request = requests.post(url, json=data, headers=headers)
    print(f"typetalk's status code is {request.status_code}.\n")


def send_message(message: str, sns_type: str) -> None:
    if sns_type == "all":
        send_typetalk(message, TYPETALK_URL, TYPETALK_TOKEN)
        send_slack(message, SLACK_URL)
    elif sns_type == "typetalk":
        send_typetalk(message, TYPETALK_URL, TYPETALK_TOKEN)
    elif sns_type == "slack":
        send_slack(message, SLACK_URL)
    else:
        ValueError("Please choose sns type in 'all', 'typetalk', 'slack'")


def main():
    args = parse_args()
    if args.message != "":
        message = args.message
    elif os.path.exists(MESSAGE_PATH):
        with open(MESSAGE_PATH, "r") as f:
            message = f.read()
    else:
        ValueError("No message")
    send_message(message, args.sns_type)


if __name__ == "__main__":
    main()
