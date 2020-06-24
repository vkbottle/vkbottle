import typing
from enum import Enum
from ..base import BaseModel


class DomainResolved(BaseModel):
    object_id: int = None
    type: "DomainResolvedType" = None

    def __hash__(self):
        return hash((self.object_id, self.type))

    def __eq__(self, other):
        return self.object_id == other.object_id and self.type == other.type


class DomainResolvedType(Enum):
    user = "user"
    group = "group"
    application = "application"
    page = "page"


class LastShortenedLink(BaseModel):
    access_key: str = None
    key: str = None
    short_url: str = None
    timestamp: int = None
    url: str = None
    views: int = None


class LinkChecked(BaseModel):
    link: str = None
    status: "LinkCheckedStatus" = None


class LinkCheckedStatus(Enum):
    not_banned = "not_banned"
    banned = "banned"
    processing = "processing"


class LinkStats(BaseModel):
    key: str = None
    stats: typing.List = None


class LinkStatsExtended(BaseModel):
    key: str = None
    stats: typing.List = None


class ShortLink(BaseModel):
    access_key: str = None
    key: str = None
    short_url: str = None
    url: str = None


class Stats(BaseModel):
    timestamp: int = None
    views: int = None


class StatsCity(BaseModel):
    city_id: int = None
    views: int = None


class StatsCountry(BaseModel):
    country_id: int = None
    views: int = None


class StatsExtended(BaseModel):
    cities: typing.List = None
    countries: typing.List = None
    sex_age: typing.List = None
    timestamp: int = None
    views: int = None


class StatsSexAge(BaseModel):
    age_range: str = None
    female: int = None
    male: int = None


DomainResolved.update_forward_refs()
LastShortenedLink.update_forward_refs()
LinkChecked.update_forward_refs()
LinkStats.update_forward_refs()
LinkStatsExtended.update_forward_refs()
ShortLink.update_forward_refs()
Stats.update_forward_refs()
StatsCity.update_forward_refs()
StatsCountry.update_forward_refs()
StatsExtended.update_forward_refs()
StatsSexAge.update_forward_refs()
