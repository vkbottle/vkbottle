from .others import SimpleResponse
from ..base import BaseModel
from ..application import Application

from ..user import User


from typing import List, Any


class DeleteAppRequests(SimpleResponse):
    pass


class GetResponse(BaseModel):
    count: int = None
    items: List[Application] = []


class Get(BaseModel):
    response: GetResponse = None


class GetCatalog(Get):
    pass


class GetFriendsListResponse(BaseModel):
    count: int = None
    items: List[User] = []


class GetFriendsList(BaseModel):
    response: GetFriendsListResponse = None


class GetLeaderboard(BaseModel):
    response: List[User] = []


class GetScopesResponse(BaseModel):
    count: int = None
    items: List[dict] = []


class GetScopes(BaseModel):
    response: GetScopesResponse = None


class GetScore(BaseModel):
    response: Any = None


class SendRequest(SimpleResponse):
    pass
