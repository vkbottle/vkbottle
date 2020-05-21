import typing
from ..base import BaseModel
from vkbottle.types import objects

SendRequest = typing.Dict


class SendRequestModel(BaseModel):
    response: SendRequest = None


class GetCatalog(BaseModel):
    count: int = None
    items: typing.List[objects.apps.App] = None


class GetCatalogModel(BaseModel):
    response: GetCatalog = None


class GetFriendsList(BaseModel):
    count: int = None
    items: typing.List[objects.users.User] = None


class GetFriendsListModel(BaseModel):
    response: GetFriendsList = None


class GetLeaderboard(BaseModel):
    count: int = None
    items: typing.List[objects.users.User] = None


class GetLeaderboardModel(BaseModel):
    response: GetLeaderboard = None


class Scope(BaseModel):
    name: str = None
    title: str = None


class GetScopes(BaseModel):
    count: int = None
    items: typing.List[Scope] = None


class GetScopesModel(BaseModel):
    response: GetScopes = None


GetScore = typing.Dict


class GetScoreModel(BaseModel):
    response: GetScore = None


class Get(BaseModel):
    count: int = None
    items: typing.List[objects.apps.App] = None


class GetModel(BaseModel):
    response: Get = None
