import typing
from ..base import BaseModel


class Activity(BaseModel):
    comments: int = None
    copies: int = None
    hidden: int = None
    likes: int = None
    subscribed: int = None
    unsubscribed: int = None


class City(BaseModel):
    count: int = None
    name: str = None
    value: int = None


class Country(BaseModel):
    code: str = None
    count: int = None
    name: str = None
    value: int = None


class Period(BaseModel):
    activity: "Activity" = None
    period_from: int = None
    period_to: int = None
    reach: "Reach" = None
    visitors: "Views" = None


class Reach(BaseModel):
    age: typing.List = None
    cities: typing.List = None
    countries: typing.List = None
    mobile_reach: int = None
    reach: int = None
    reach_subscribers: int = None
    sex: typing.List = None
    sex_age: typing.List = None


class SexAge(BaseModel):
    count: int = None
    value: str = None


class Views(BaseModel):
    age: typing.List = None
    cities: typing.List = None
    countries: typing.List = None
    mobile_views: int = None
    sex: typing.List = None
    sex_age: typing.List = None
    views: int = None
    visitors: int = None


class WallpostStat(BaseModel):
    hide: int = None
    join_group: int = None
    links: int = None
    reach_subscribers: int = None
    reach_total: int = None
    report: int = None
    to_group: int = None
    unsubscribe: int = None


Activity.update_forward_refs()
City.update_forward_refs()
Country.update_forward_refs()
Period.update_forward_refs()
Reach.update_forward_refs()
SexAge.update_forward_refs()
Views.update_forward_refs()
WallpostStat.update_forward_refs()
