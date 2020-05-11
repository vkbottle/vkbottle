import typing
from ..base import BaseModel

SendRequest = typing.Dict


class SendRequestModel(BaseModel):
    response: SendRequest = None


class GetCatalog(BaseModel):
    count: int = None
    items: typing.List = None


class GetCatalogModel(BaseModel):
    response: GetCatalog = None


class GetFriendsList(BaseModel):
    count: int = None
    items: typing.List = None


class GetFriendsListModel(BaseModel):
    response: GetFriendsList = None


class GetLeaderboard(BaseModel):
    count: int = None
    items: typing.List = None


class GetLeaderboardModel(BaseModel):
    response: GetLeaderboard = None


class GetScopes(BaseModel):
    count: int = None
    items: typing.List = None


class GetScopesModel(BaseModel):
    response: GetScopes = None


GetScore = typing.Dict


class GetScoreModel(BaseModel):
    response: GetScore = None


class Get(BaseModel):
    count: int = None
    items: typing.List = None


class GetModel(BaseModel):
    response: Get = None
