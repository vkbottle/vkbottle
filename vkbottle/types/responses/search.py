import typing
from ..base import BaseModel


class GetHints(BaseModel):
    count: int = None
    items: typing.List = None
    suggested_queries: typing.List = None


class GetHintsModel(BaseModel):
    response: GetHints = None
