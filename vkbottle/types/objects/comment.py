import typing
from enum import Enum
from ..base import BaseModel
from vkbottle.types import objects


class Thread(BaseModel):
    can_post: bool = None
    count: int = None
    groups_can_post: bool = None
    items: typing.List = None
    show_reply_button: bool = None


Thread.update_forward_refs()
