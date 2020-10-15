import typing
from ..base import BaseModel
from vkbottle.types.objects import storage

Get = typing.Union[typing.List[storage.Value], str]


class GetModel(BaseModel):
    response: Get = None


GetKeys = typing.List[str]


class GetKeysModel(BaseModel):
    response: GetKeys = None
