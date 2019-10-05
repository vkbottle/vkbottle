from ..base import BaseModel
from ..additional import PhotoSizes
import typing


class PrettyCard(BaseModel):
    card_id: str = None
    link_url: str = None
    title: str = None
    images: typing.List[PhotoSizes] = None
    button: typing.Any = None
    price: str = None
    price_old: str = None


class PrettyCards(BaseModel):
    cards: typing.List[PrettyCard] = None
