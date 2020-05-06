import typing
from ..base import BaseModel

Get = typing.Dict


class GetModel(BaseModel):
    response: Get = None


GetKeys = typing.List[str]


class GetKeysModel(BaseModel):
    response: GetKeys = None
