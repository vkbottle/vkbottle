import typing
import enum
from ..base import BaseModel
from vkbottle.types import objects


class GetHints(BaseModel):
    count: int = None
    items: typing.List = None
    suggested_queries: typing.List = None


class GetHintsModel(BaseModel):
    response: GetHints = None
