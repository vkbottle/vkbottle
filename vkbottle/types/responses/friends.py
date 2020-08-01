import typing
import enum
from ..base import BaseModel
from vkbottle.types import objects


class Search(BaseModel):
    count: int = None
    items: typing.List[objects.users.User] = None


class SearchModel(BaseModel):
    response: Search = None


class AddList(BaseModel):
    list_id: int = None


class AddListModel(BaseModel):
    response: AddList = None


class Add(enum.IntEnum):
    sent = 1
    approved = 2
    resending = 4


class AddModel(BaseModel):
    response: Add = None


AreFriends = typing.List[objects.friends.FriendStatus]


class AreFriendsModel(BaseModel):
    response: AreFriends = None


class Delete(BaseModel):
    success: objects.base.OkResponse = None
    friend_deleted: int = None
    out_request_deleted: int = None
    in_request_deleted: int = None
    suggestion_deleted: int = None


class DeleteModel(BaseModel):
    response: Delete = None


GetAppUsers = typing.List[int]


class GetAppUsersModel(BaseModel):
    response: GetAppUsers = None


GetByPhones = typing.List[objects.users.UserXtrPhone]


class GetByPhonesModel(BaseModel):
    response: GetByPhones = None


class GetLists(BaseModel):
    count: int = None
    items: typing.List[objects.friends.FriendsList] = None


class GetListsModel(BaseModel):
    response: GetLists = None


GetMutual = typing.List[int]


class GetMutualModel(BaseModel):
    response: GetMutual = None


GetOnline = typing.List[int]


class GetOnlineModel(BaseModel):
    response: GetOnline = None


GetRecent = typing.List[int]


class GetRecentModel(BaseModel):
    response: GetRecent = None


class FriendRequest(BaseModel):
    user_id: int = None
    mutual: objects.friends.RequestsMutual = None
    message: objects.friends.RequestsXtrMessage = None


class GetRequests(BaseModel):
    count: int = None
    items: typing.List[FriendRequest] = None
    count_unread: int = None


class GetRequestsModel(BaseModel):
    response: GetRequests = None


class GetSuggestions(BaseModel):
    count: int = None
    items: typing.List[objects.users.User] = None


class GetSuggestionsModel(BaseModel):
    response: GetSuggestions = None


class Get(BaseModel):
    count: int = None
    items: typing.List[typing.Union[int, objects.users.UserFull]] = None


class GetModel(BaseModel):
    response: Get = None
