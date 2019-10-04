from .others import SimpleResponse
from ..base import BaseModel

from ..additional import Place
from ..community import Community
from ..user import User

import typing


class AddAddress(BaseModel):
    response: Place = None


class AddCallbackServerResponse(BaseModel):
    server_id: int = None


class AddCallbackServer(BaseModel):
    response: AddCallbackServerResponse = None


class AddLinkResponse(BaseModel):
    id: int = None
    url: str = None
    edit_title: int = None
    name: str = None
    desc: str = None
    image_processing: int = None


class AddLink(BaseModel):
    response: AddLinkResponse = None


class ApproveRequest(SimpleResponse):
    pass


class Ban(SimpleResponse):
    pass


class Create(BaseModel):
    response: Community = None


class DeleteAddress(SimpleResponse):
    pass


class DeleteCallbackServer(SimpleResponse):
    pass


class DeleteLink(SimpleResponse):
    pass


class DisableOnline(SimpleResponse):
    pass


class Edit(SimpleResponse):
    pass


class EditAddress(BaseModel):
    response: Place = None


class EditCallbackServer(SimpleResponse):
    pass


class EditLink(SimpleResponse):
    pass


class EditManager(SimpleResponse):
    pass


class EnableOnline(SimpleResponse):
    pass


class GetResponse(BaseModel):
    count: int = None
    items: typing.List[Community] = None


class Get(BaseModel):
    response: GetResponse = None


class GetAddressesResponse(BaseModel):
    count: int = None
    items: typing.List[Place] = None


class GetAdresses(BaseModel):
    response: GetAddressesResponse = None


class GetBannedResponse(BaseModel):
    count: int = None
    items: typing.List = None


class GetBanned(BaseModel):
    response: GetBannedResponse = None


class GetById(BaseModel):
    response: typing.List[Community] = None


class GetCallbackConfirmationCodeResponse(BaseModel):
    code: str = None


class GetCallbackConfirmationCode(BaseModel):
    response: GetCallbackConfirmationCodeResponse = None


class GetCallbackServersItem(BaseModel):
    id: int = None
    title: str = None
    creator_id: int = None
    url: str = None
    secret_key: str = None
    status: str = None


class GetCallbackServersResponse(BaseModel):
    count: int = None
    items: typing.List[GetCallbackServersItem] = None


class GetCallbackServers(BaseModel):
    response: GetCallbackServersResponse = None


class GetCallbackSettingsResponse(BaseModel):
    api_version: str = None
    events: typing.Dict[str, int] = None


class GetCallbackSettings(BaseModel):
    response: GetCallbackSettingsResponse = None


class GetCatalogResponse(BaseModel):
    count: int = None
    items: typing.List[Community] = None


class GetCatalog(BaseModel):
    response: GetCatalogResponse = None


class GetCatalogInfoResponse(BaseModel):
    enabled: int = None
    id: int = None
    name: str = None
    subcategories: list = None
    page_count: int = None
    page_privews: list = None


class GetCatalogInfo(BaseModel):
    response: GetCatalogInfoResponse = None


class GetInvitedUsersResponse(BaseModel):
    count: int = None
    items: typing.List[User] = None


class GetInvitedUsers(BaseModel):
    response: GetInvitedUsersResponse = None


class GetInvitesResponse(BaseModel):
    count: int = None
    items: typing.List[Community] = None


class GetInvites(BaseModel):
    response: GetInvitesResponse = None


class GetLongPollServerResponse(BaseModel):
    key: str = None
    server: str = None
    ts: int = None


class GetLongPollServer(BaseModel):
    response: GetLongPollServerResponse = None


class GetLongPollSettingsResponse(BaseModel):
    events: typing.Dict[str, int] = None
    is_enabled: bool = None
    api_version: str = None


class GetLongPollSettings(BaseModel):
    response: GetLongPollSettingsResponse = None


class GetMembersResponse(BaseModel):
    count: int = None
    items: typing.List[int] = None


class GetMembers(BaseModel):
    response: GetMembersResponse = None


class GetOnlineStatusResponse(BaseModel):
    status: str = None
    minutes: int = None


class GetOnlineStatus(BaseModel):
    response: GetOnlineStatusResponse = None


class GetRequestsResponse(BaseModel):
    count: int = None
    items: typing.List[User] = None


class GetRequests(BaseModel):
    response: GetRequestsResponse = None


class GetSettings(BaseModel):
    response: typing.Any = None


class GetTokenPermissionsSetting(BaseModel):
    setting: int = None
    name: str = None


class GetTokenPermissionsResponse(BaseModel):
    mask: int = None
    settings: typing.List[GetTokenPermissionsSetting] = None


class Invite(SimpleResponse):
    pass


class IsMemberResponse(BaseModel):
    member: int = None
    can_invite: int = None


class IsMember(BaseModel):
    response: IsMemberResponse = None


class Join(SimpleResponse):
    pass


class Leave(SimpleResponse):
    pass


class RemoveUser(SimpleResponse):
    pass


class ReorderLink(SimpleResponse):
    pass


class SearchResponse(BaseModel):
    count: int = None
    items: typing.List[Community] = None


class Search(BaseModel):
    response: SearchResponse = None


class SetCallbackSettings(SimpleResponse):
    pass


class SetLongPollSettings(SimpleResponse):
    pass


class SetSettings(SimpleResponse):
    pass


class Unban(SimpleResponse):
    pass
