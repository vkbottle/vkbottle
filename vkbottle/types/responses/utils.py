import typing
from ..base import BaseModel
from vkbottle.types import objects

ResolveScreenName = objects.utils.DomainResolved


class ResolveScreenNameModel(BaseModel):
    response: ResolveScreenName = None


CheckLink = objects.utils.LinkChecked


class CheckLinkModel(BaseModel):
    response: CheckLink = None


class GetLastShortenedLinks(BaseModel):
    count: int = None
    items: typing.List[objects.utils.LastShortenedLink] = None


class GetLastShortenedLinksModel(BaseModel):
    response: GetLastShortenedLinks = None


GetLinkStats = objects.utils.LinkStats


class GetLinkStatsModel(BaseModel):
    response: GetLinkStats = None


GetServerTime = typing.Dict


class GetServerTimeModel(BaseModel):
    response: GetServerTime = None


GetShortLink = objects.utils.ShortLink


class GetShortLinkModel(BaseModel):
    response: GetShortLink = None
