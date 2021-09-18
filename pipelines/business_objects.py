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
class GetOrCreateSlackMsg:
    source_thread_id: str
    source_type: str
    body: str
    info: dict


@dataclass
class SlackOutboundMessage:
    msg_id: str
    body: str
    channel: str
    info: dict
    thread_ts: Optional[str] = None
