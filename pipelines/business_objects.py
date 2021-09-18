from typing import Optional
from dataclasses import dataclass


@dataclass
class InitialInputData:
    source_thread_id: str
    source_type: str
    body: str
    info: dict
    msg_id: str
    payload: dict


@dataclass
class GetSlackThreadData:
    source_thread_id: str
    source_type: str
    body: str
    info: dict


@dataclass
class DispatchData:
    source_thread_id: str
    source_type: str
    body: str
    info: dict
    thread_ts: Optional[str] = None


@dataclass
class SlackOutboundMessageData:
    source_thread_id: str
    source_type: str
    info: dict
    channel: str
    text: str
    thread_ts: Optional[str]
