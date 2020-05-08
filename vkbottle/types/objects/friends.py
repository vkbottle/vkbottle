from . import base
import typing
from ..base import BaseModel


class FriendStatus(BaseModel):
    friend_status: int = None
    read_state: "base.BoolInt" = None
    request_message: str = None
    sign: str = None
    user_id: int = None


class FriendsList(BaseModel):
    id: int = None
    name: str = None


class MutualFriend(BaseModel):
    common_count: int = None
    common_friends: typing.List = None
    id: int = None


class Requests(BaseModel):
    _from: str = None
    mutual: "RequestsMutual" = None
    user_id: int = None


class RequestsMutual(BaseModel):
    count: int = None
    users: typing.List = None


class RequestsXtrMessage(BaseModel):
    _from: str = None
    message: str = None
    mutual: "RequestsMutual" = None
    user_id: int = None


FriendStatus.update_forward_refs()
FriendsList.update_forward_refs()
MutualFriend.update_forward_refs()
Requests.update_forward_refs()
RequestsMutual.update_forward_refs()
RequestsXtrMessage.update_forward_refs()
