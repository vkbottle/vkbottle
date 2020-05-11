import typing
from ..base import BaseModel
from vkbottle.types import objects

Get = typing.List[objects.stats.Period]


class GetModel(BaseModel):
    response: Get = None


GetPostReach = typing.List[objects.stats.WallpostStat]


class GetPostReachModel(BaseModel):
    response: GetPostReach = None
