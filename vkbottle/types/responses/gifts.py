import typing
import enum
from ..base import BaseModel
from vkbottle.types import objects


class Get(BaseModel):
    count: int = None
    items: typing.List = None


class GetModel(BaseModel):
    response: Get = None
