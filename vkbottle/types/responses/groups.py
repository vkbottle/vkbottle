from .others import SimpleResponse
from ..base import BaseModel

from ..additional import Place
from ..community import Community
from ..user import User

from typing import Any, List, Dict


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
    items: List[Community] = []


class Get(BaseModel):
    response: GetResponse = None


class GetAddressesResponse(BaseModel):
    count: int = None
    items: List[Place] = []


class GetAdresses(BaseModel):
    response: GetAddressesResponse = None


class GetBannedResponse(BaseModel):
    count: int = None
    items: List = []


class GetBanned(BaseModel):
    response: GetBannedResponse = None


class GetById(BaseModel):
    response: List[Community] = []


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
    items: List[GetCallbackServersItem] = []


class GetCallbackServers(BaseModel):
    response: GetCallbackServersResponse = None


class GetCallbackSettingsResponse(BaseModel):
    api_version: str = None
    events: Dict[str, int] = {}


class GetCallbackSettings(BaseModel):
    response: GetCallbackSettingsResponse = None


class GetCatalogResponse(BaseModel):
    count: int = None
    items: List[Community] = []


class GetCatalog(BaseModel):
    response: GetCatalogResponse = None


class GetCatalogInfoResponse(BaseModel):
    enabled: int = None
    id: int = None
    name: str = None
    subcategories: list = []
    page_count: int = None
    page_privews: list = []


class GetCatalogInfo(BaseModel):
    response: GetCatalogInfoResponse = None


class GetInvitedUsersResponse(BaseModel):
    count: int = None
    items: List[User] = []


class GetInvitedUsers(BaseModel):
    response: GetInvitedUsersResponse = None


class GetInvitesResponse(BaseModel):
    count: int = None
    items: List[Community] = []


class GetInvites(BaseModel):
    response: GetInvitesResponse = None


class GetLongPollServerResponse(BaseModel):
    key: str = None
    server: str = None
    ts: int = None


class GetLongPollServer(BaseModel):
    response: GetLongPollServerResponse = None


class GetLongPollSettingsResponse(BaseModel):
    events: Dict[str, int] = {}
    is_enabled: bool = None
    api_version: str = None


class GetLongPollSettings(BaseModel):
    response: GetLongPollSettingsResponse = None


class GetMembersResponse(BaseModel):
    count: int = None
    items: List[int] = []


class GetMembers(BaseModel):
    response: GetMembersResponse = None


class GetOnlineStatusResponse(BaseModel):
    status: str = None
    minutes: int = None


class GetOnlineStatus(BaseModel):
    response: GetOnlineStatusResponse = None


class GetRequestsResponse(BaseModel):
    count: int = None
    items: List[User] = []


class GetRequests(BaseModel):
    response: GetRequestsResponse = None


class GetSettings(BaseModel):
    response: Any = None


class GetTokenPermissionsSetting(BaseModel):
    setting: int = None
    name: str = None


class GetTokenPermissionsResponse(BaseModel):
    mask: int = None
    settings: List[GetTokenPermissionsSetting] = []


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
    items: List[Community] = []


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
