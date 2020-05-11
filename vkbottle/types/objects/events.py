from . import groups
import typing
from ..base import BaseModel


class EventAttach(BaseModel):
    address: str = None
    button_text: str = None
    friends: typing.List = None
    id: int = None
    is_favorite: bool = None
    member_status: int = None
    text: str = None
    time: int = None


EventAttach.update_forward_refs()
