import typing
from ..base import BaseModel
from vkbottle.types import objects

SendMessage = typing.List[objects.notifications.SendMessageItem]


class SendMessageModel(BaseModel):
    response: SendMessage = None


class Get(BaseModel):
    count: int = None
    items: typing.List[objects.notifications.Notification] = None
    profiles: typing.List[objects.users.User] = None
    groups: typing.List[objects.groups.Group] = None
    last_viewed: int = None
    photos: typing.List[objects.photos.Photo] = None
    videos: typing.List[objects.video.Video] = None
    apps: typing.List[objects.apps.App] = None
    next_from: str = None
    ttl: int = None


class GetModel(BaseModel):
    response: Get = None


MarkAsViewed = objects.base.BoolInt


class MarkAsViewedModel(BaseModel):
    response: MarkAsViewed = None
