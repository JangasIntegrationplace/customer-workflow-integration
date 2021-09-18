from typing import Optional
from abc import ABC, abstractmethod
from ._immutable import xdict, freeze
from .layers import BaseLayer, SentimentAnalysisLayer, GroupContentLayer
from .settings import DB_HANDLER


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
        DB_HANDLER.create_initial_input(self.data)


class DispatchController(BaseController):
    def handler(self):
        self.process_data()


class GetSlackThreadController(BaseController):
    def handler(self):
        self.process_data()
        return DB_HANDLER.retrieve_slack_thread(self.data)


class ContentGroupController(BaseController):
    layer = GroupContentLayer


class SentimentAnalysisController(BaseController):
    layer = SentimentAnalysisLayer


class OutputStreamController(BaseController):
    def handler(self):
        self.process_data()
        DB_HANDLER.create_output_stream(self.data)
