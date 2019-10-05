from .others import SimpleResponse
from ..base import BaseModel
from ..attachments.gift import Gift


import typing


class GetResponseItem(BaseModel):
    id: int = None
    from_id: int = None
    message: str = None
    date: int = None
    gift: Gift = None
    privacy: int = None
    gift_hash: str = None


class GetResponse(BaseModel):
    count: int = None
    items: typing.List[GetResponseItem] = None


class Get(BaseModel):
    response: GetResponse = None
