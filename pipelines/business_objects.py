from typing import Optional
from dataclasses import dataclass


@dataclass
class InitialInputData:
    msg_id: str
    payload: dict
    source: str


@dataclass
class GetOrCreateSlackMsg(InitialInputData):
    pass


@dataclass
class SlackOutboundMessage:
    msg_id: str
    body: str
    channel: str
    info: dict
    thread_ts: Optional[str] = None
