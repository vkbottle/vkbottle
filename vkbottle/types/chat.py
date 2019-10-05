from .base import BaseModel

import typing

# https://vk.com/dev/objects/chat


class ChatPushSettings(BaseModel):
    sound: int = None
    disabled_until: int = None
    disabled_forever: int = None
    no_sound: bool = None


class Chat(BaseModel):
    id: int = None
    type: str = None
    title: str = None
    admin_id: int = None
    users: typing.List[int] = None
    push_settings: ChatPushSettings = None
    photo_50: str = None
    photo_100: str = None
    photo_200: str = None
    left: int = None
    kicked: int = None
