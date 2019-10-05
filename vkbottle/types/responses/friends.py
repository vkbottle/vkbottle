from .others import SimpleResponse
from ..base import BaseModel

from ..user import User

import typing


class Add(SimpleResponse):
    pass


class AddListResponse(BaseModel):
    list_id: int = None


class AddList(BaseModel):
    response: AddListResponse = None


class AreFriendsResponse(BaseModel):
    user_id: int = None
    friend_status: int = None
    sign: str = None


class AreFriends(BaseModel):
    response: typing.List[AreFriendsResponse] = None


class DeleteResponse(BaseModel):
    success: int = None
    friend_deleted: int = None
    out_request_deleted: int = None
    in_request_deleted: int = None
    suggestion_deleted: int = None


class Delete(BaseModel):
    response: DeleteResponse = None


class DeleteAllRequests(SimpleResponse):
    pass


class DeleteList(SimpleResponse):
    pass


class Edit(SimpleResponse):
    pass


class EditList(SimpleResponse):
    pass


class GetResponse(BaseModel):
    count: int = None
    items: typing.List[User] = None


class Get(BaseModel):
    response: GetResponse = None


class GetAppUsers(BaseModel):
    response: typing.List[int] = None


class GetByPhones(BaseModel):
    response: typing.List[User] = None


class GetListsResponseItem(BaseModel):
    name: str = None
    id: int = None


class GetListsResponse(BaseModel):
    count: int = None
    items: typing.List[GetListsResponseItem] = None


class GetLists(BaseModel):
    response: GetListsResponse = None


class GetMutual(BaseModel):
    response: typing.List[int] = None


class GetOnline(BaseModel):
    response: typing.List[int] = None


class GetRecent(BaseModel):
    response: typing.List[int] = None


class GetRequestsItem(User):
    mutual: typing.Any = None
    track_code: str = None


class GetRequestsResponse(BaseModel):
    count: int = None
    items: typing.List[GetRequestsItem] = None


class GetRequests(BaseModel):
    response: GetRequestsResponse = None


class GetSuggestionsResponse(BaseModel):
    count: int = None
    items: typing.List[User] = None


class GetSuggestions(BaseModel):
    response: GetSuggestionsResponse = None


class Search(BaseModel):
    response: GetSuggestionsResponse = None
