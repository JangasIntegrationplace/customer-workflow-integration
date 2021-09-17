from typing import Any, Optional
from ._immutable import xdict, freeze
from .layers import BaseLayer, SentimentAnalysisLayer, GroupContentLayer
from .settings import pipeline


class BaseController:
    layer: Optional[BaseLayer] = None

    def __init__(self, data: dict, *args, **kwargs):
        # Just for security purpose on debugging:
        # Never override input data.
        self.raw_data = freeze(xdict(data))
        self.data = data

    def process_data(self, data: Any):
        if self.layer:
            self.data[self.layer.__name__] = self.layer.proceed(data)
        return self.data

    def handler(self):
        self.process_data()


class InputStreamController(BaseController):
    def handler(self):
        self.process_data()
        pipeline["DB_HANDLER"].create_initial_input(self.data)
        # TODO: Important: self.data must contain key "source"


class ContentGroupController(BaseController):
    layer = GroupContentLayer


class SentimentAnalysisController(BaseController):
    layer = SentimentAnalysisLayer


class OutputStreamController(BaseController):
    def handler(self):
        self.process_data()
        pipeline["DB_HANDLER"].create_output_stream(self.data)
