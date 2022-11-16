import argparse
import json
import os

import requests
from dotenv import load_dotenv

load_dotenv(".env")

MESSAGE_PATH = "message.txt"


def parse_args():
    parser = argparse.ArgumentParser()
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


class AutoSender:
    SNSs = ["typetalk", "slack"]

    def __init__(self, args, message) -> None:
        self.message = message
        self.sns_type = args.sns_type
        self.typetalk_url = os.environ.get("TYPETALK_URL")
        self.typetalk_token = os.environ.get("TYPETALK_TOKEN")
        self.slack_url = os.environ.get("SLACK_URL")

    def send_message(self) -> None:
        if self.sns_type == "all":
            self._send_typetalk()
            self._send_slack()
        elif self.sns_type == "typetalk":
            self._send_typetalk()
        elif self.sns_type == "slack":
            self._send_slack()
        else:
            raise ValueError("Please choose sns type in 'all', 'typetalk', 'slack'")

    def _send_slack(self) -> None:
        data = json.dumps(
            {
                "text": self.message,
            }
        )
        request = requests.post(
            self.slack_url,
            data=data,
        )
        self._check_status_code(request)

    def _send_typetalk(self) -> None:
        data = {"message": self.message}
        headers = {"X-TYPETALK-TOKEN": self.typetalk_token}
        request = requests.post(self.typetalk_url, json=data, headers=headers)
        self._check_status_code(request)

    def _check_status_code(self, request) -> None:
        print(f"{self.sns_type}'s status code is {request.status_code}.")

    def check_message(self) -> None:
        print(self.message)

    @classmethod
    def check_SNSs(cls) -> None:
        print(f"this autosender can send to {cls.SNSs}.")

    @staticmethod
    def describe() -> None:
        print("this is auto sender for me.")


def main():
    args = parse_args()
    if args.message != "":
        message = args.message
    elif os.path.exists(MESSAGE_PATH):
        with open(MESSAGE_PATH, "r") as f:
            message = f.read()
    else:
        raise ValueError("No message")
    sender = AutoSender(args, message)
    sender.send_message()


if __name__ == "__main__":
    main()
