import typing
from ..base import BaseModel
from vkbottle.types import objects


class Search(BaseModel):
    count: int = None
    items: typing.List[objects.users.User] = None


class SearchModel(BaseModel):
    response: Search = None


class GetFollowers(BaseModel):
    count: int = None
    items: typing.List[objects.users.User] = None


class GetFollowersModel(BaseModel):
    response: GetFollowers = None


class GetSubscriptions(BaseModel):
    users: objects.users.UsersArray = None
    groups: objects.groups.GroupsArray = None


class GetSubscriptionsModel(BaseModel):
    response: GetSubscriptions = None


Get = typing.List[objects.users.UserXtrCounters]


class GetModel(BaseModel):
    response: Get = None


IsAppUser = objects.base.BoolInt


class IsAppUserModel(BaseModel):
    response: IsAppUser = None
