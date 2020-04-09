import typing
from enum import Enum
from ..base import BaseModel
from vkbottle.types import objects


class Gift(BaseModel):
    date: int = None
    from_id: int = None
    gift: "Layout" = None
    gift_hash: str = None
    id: int = None
    message: str = None
    privacy: "GiftPrivacy" = None


class GiftPrivacy(Enum):
    _0 = "0"
    _1 = "1"
    _2 = "2"


class Layout(BaseModel):
    id: int = None
    thumb_256: str = None
    thumb_48: str = None
    thumb_96: str = None


Gift.update_forward_refs()
Layout.update_forward_refs()
