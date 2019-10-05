from .base import BaseModel
from enum import Enum

from .chat import ChatPushSettings
from .attachments import Photo

import typing


class ConversationCanWrite(BaseModel):
    allowed: bool = None
    reason: int = None


class Peer(BaseModel):
    id: int = None
    type: str = None
    local_id: int = None


class ConversationChatSettings(BaseModel):
    members_count: int = None
    title: str = None
    pinned_message: typing.Any = None
    state: str = None
    photo: Photo = None
    active_ids: typing.List[int] = None


class Conversation(BaseModel):
    peer: Peer = None
    in_read: int = None
    out_read: int = None
    unread_count: int = None
    important: bool = None
    unanswered: bool = None
    push_settings: ChatPushSettings = None
    can_write: ConversationCanWrite = None
    chat_settings: ConversationChatSettings = None
