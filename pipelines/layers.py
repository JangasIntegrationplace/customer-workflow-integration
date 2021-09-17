from abc import ABC, abstractclassmethod


class BaseLayer(ABC):
    @abstractclassmethod
    def proceed(cls, *args, **kwargs):
        pass


class SentimentAnalysisLayer(BaseLayer):
    def proceed(cls, message: str):
        from random import randint
        return {"mode": "positive" if bool(randint(0, 1)) else "negative"}


class GroupContentLayer(BaseLayer):
    def proceed(cls, message: str):
        return {"group": None}
