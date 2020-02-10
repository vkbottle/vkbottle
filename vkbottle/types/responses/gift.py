from .others import SimpleResponse
from ..base import BaseModel
from ..attachments.gift import Gift

from typing import List


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
    items: List[GetResponseItem] = []


class Get(BaseModel):
    response: GetResponse = None
