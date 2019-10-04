from .others import SimpleResponse
from ..base import BaseModel
from ..application import Application

from ..user import User


import typing


class DeleteAppRequests(SimpleResponse):
    pass


class GetResponse(BaseModel):
    count: int = None
    items: typing.List[Application] = None


class Get(BaseModel):
    response: GetResponse = None


class GetCatalog(Get):
    pass


class GetFriendsListResponse(BaseModel):
    count: int = None
    items: typing.List[User] = None


class GetFriendsList(BaseModel):
    response: GetFriendsListResponse = None


class GetLeaderboard(BaseModel):
    response: typing.List[User] = None


class GetScopesResponse(BaseModel):
    count: int = None
    items: typing.List[dict] = None


class GetScopes(BaseModel):
    response: GetScopesResponse = None


class GetScore(BaseModel):
    response: typing.Any = None


class SendRequest(SimpleResponse):
    pass
