import typing
from enum import Enum
from ..base import BaseModel
from vkbottle.types import objects


class PrettyCard(BaseModel):
    button: str = None
    button_text: str = None
    card_id: str = None
    images: typing.List = None
    link_url: str = None
    photo: str = None
    price: str = None
    price_old: str = None
    title: str = None


PrettyCard.update_forward_refs()
