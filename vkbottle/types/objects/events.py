from . import groups
import typing
from enum import Enum
from ..base import BaseModel
from vkbottle.types import objects


class EventAttach(BaseModel):
    address: str = None
    button_text: str = None
    friends: typing.List = None
    id: int = None
    is_favorite: bool = None
    member_status: "groups.GroupFullMemberStatus" = None
    text: str = None
    time: int = None


EventAttach.update_forward_refs()
