from typing import Optional
from slack_sdk.web import WebClient


class Slack:
    @classmethod
    def get_client(cls, slack_bot_token: str):
        client = WebClient(token=slack_bot_token)
        return client

    @classmethod
    def post_message(cls, channel: str, text: str, *,
                     slack_bot_token: str, thread_ts: Optional[str] = None):
        client = cls.get_client(slack_bot_token)
        return client.chat_postMessage(
            channel=channel,
            text=text,
            thread_ts=thread_ts
        )
