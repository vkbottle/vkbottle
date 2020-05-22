import typing
from ..base import BaseModel
from vkbottle.types import objects

GetHints = typing.List[objects.search.Hint]


class GetHintsModel(BaseModel):
    response: GetHints = None
