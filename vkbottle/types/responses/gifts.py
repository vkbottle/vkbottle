import typing
from ..base import BaseModel
from vkbottle.types import objects


class Get(BaseModel):
    count: int = None
    items: typing.List[objects.gifts.Gift] = None


class GetModel(BaseModel):
    response: Get = None
