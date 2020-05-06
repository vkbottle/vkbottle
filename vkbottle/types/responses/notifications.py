import typing
from ..base import BaseModel
from vkbottle.types import objects

SendMessage = typing.List[objects.notifications.SendMessageItem]


class SendMessageModel(BaseModel):
    response: SendMessage = None


class Get(BaseModel):
    count: int = None
    items: typing.List = None
    profiles: typing.List = None
    groups: typing.List = None
    last_viewed: int = None
    photos: typing.List = None
    videos: typing.List = None
    apps: typing.List = None
    next_from: str = None
    ttl: int = None


class GetModel(BaseModel):
    response: Get = None


MarkAsViewed = objects.base.BoolInt


class MarkAsViewedModel(BaseModel):
    response: MarkAsViewed = None
