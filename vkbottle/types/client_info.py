import enum
import typing
from .base import BaseModel


class ButtonActions(enum.Enum):
    text = "text"
    location = "location"
    vkpay = "vkpay"
    open_app = "open_app"
    open_link = "open_link"
    open_photo = "open_photo"
    callback = "callback"


class ClientInfo(BaseModel):
    button_actions: typing.List[ButtonActions] = None
    keyboard: bool = None
    inline_keyboard: bool = None
    lang_id: int = None
