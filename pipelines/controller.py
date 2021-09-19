import json
from typing import Optional
from abc import ABC, abstractmethod
from ._immutable import xdict, freeze
from .layers import BaseLayer, SentimentAnalysisLayer, GroupContentLayer
from .business_objects import GetSlackThreadData, DispatchData, SlackOutboundMessageData
from . import settings
from .slack import Slack


class BaseController(ABC):
    layer: Optional[BaseLayer] = None

    def __init__(self, data: dict, *args, **kwargs):
        # Just for security purpose on debugging:
        # Never override input data.
        self.raw_data = freeze(xdict(data))
        self.data = data

    @abstractmethod
    def process_data(self, *args, **kwargs):
        pass

    @abstractmethod
    def handler(self, *args, **kwargs):
        pass


class InputStreamController(BaseController):
    def handler(self):
        self.process_data()
        settings.DB_HANDLER.create_initial_input(self.data)


class DispatchController(BaseController):
    def process_data(self):
        self.data = DispatchData(
            source_thread_id=self.data["source_thread_id"],
            source_type=self.data["source_type"],
            body=self.data["body"],
            info=self.data["info"],
            thread_ts=self.data["thread_ts"]
        )


class GetSlackThreadController(BaseController):
    def process_data(self):
        self.data = GetSlackThreadData(
            source_thread_id=self.data["source_thread_id"],
            source_type=self.data["source_type"],
            body=self.data["body"],
            info=self.data["info"]
        )

    def handler(self):
        self.process_data()
        return settings.DB_HANDLER.retrieve_slack_thread(self.data)


class ContentGroupController(BaseController):
    layer = GroupContentLayer


class SentimentAnalysisController(BaseController):
    layer = SentimentAnalysisLayer


class OutputStreamController(BaseController):
    def process_data(self, channel, text, thread_ts):
        self.data = SlackOutboundMessageData(
            source_thread_id=self.data["source_thread_id"],
            source_type=self.data["source_type"],
            info=self.data["info"],
            text=text,
            channel=channel,
            thread_ts=thread_ts
        )

    @abstractmethod
    def get_channel(self):
        pass

    def handler(self):
        channel = self.get_channel()

        json_info = json.dumps(self.data["info"], indent=True)
        text = (
            "**New Thread**\n\n"
            f"**Info**\n{json_info}\n\n"
            f"**text**\n{self.data['body']}"
        )

        slack_message = Slack.post_message(
            channel, text,
            slack_bot_token=settings.SLACK_BOT_TOKEN,
            thread_ts=self.data["thread_ts"]
        )

        thread_ts = self.data.get("thread_ts", slack_message.data["ts"])

        self.process_data(channel, text, thread_ts)
        settings.DB_HANDLER.create_output_stream(self.data)
