from ..base import BaseModel
from ..additional import PhotoSizes

from typing import List, Any


class PrettyCard(BaseModel):
    card_id: str = None
    link_url: str = None
    title: str = None
    images: List[PhotoSizes] = []
    button: Any = None
    price: str = None
    price_old: str = None


class PrettyCards(BaseModel):
    cards: List[PrettyCard] = []
