from .others import SimpleResponse
from ..base import BaseModel

from ..user import User

from typing import List, Any


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
    items: List[User] = []


class Get(BaseModel):
    response: GetResponse = None


class GetAppUsers(BaseModel):
    response: List[int] = []


class GetByPhones(BaseModel):
    response: List[User] = []


class GetListsResponseItem(BaseModel):
    name: str = None
    id: int = None


class GetListsResponse(BaseModel):
    count: int = None
    items: List[GetListsResponseItem] = []


class GetLists(BaseModel):
    response: GetListsResponse = None


class GetMutual(BaseModel):
    response: List[int] = []


class GetOnline(BaseModel):
    response: List[int] = []


class GetRecent(BaseModel):
    response: List[int] = []


class GetRequestsItem(User):
    mutual: Any = None
    track_code: str = None


class GetRequestsResponse(BaseModel):
    count: int = None
    items: List[GetRequestsItem] = []


class GetRequests(BaseModel):
    response: GetRequestsResponse = None


class GetSuggestionsResponse(BaseModel):
    count: int = None
    items: List[User] = []


class GetSuggestions(BaseModel):
    response: GetSuggestionsResponse = None


class Search(BaseModel):
    response: GetSuggestionsResponse = None
