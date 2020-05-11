import typing
from ..base import BaseModel


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
