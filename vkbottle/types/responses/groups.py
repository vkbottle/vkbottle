import typing
from ..base import BaseModel
from vkbottle.types import objects


class Search(BaseModel):
    count: int = None
    items: typing.List[objects.groups.Group] = None


class SearchModel(BaseModel):
    response: Search = None


class AddCallbackServer(BaseModel):
    server_id: int = None


class AddCallbackServerModel(BaseModel):
    response: AddCallbackServer = None


AddLink = objects.groups.GroupLink


class AddLinkModel(BaseModel):
    response: AddLink = None


Create = objects.groups.Group


class CreateModel(BaseModel):
    response: Create = None


EditAddress = objects.groups.Address


class EditAddressModel(BaseModel):
    response: EditAddress = None


class GetAddresses(BaseModel):
    count: int = None
    items: typing.List[objects.groups.Address] = None


class GetAddressesModel(BaseModel):
    response: GetAddresses = None


class GetBanned(BaseModel):
    count: int = None
    items: typing.List[objects.groups.GroupBanInfo] = None


class GetBannedModel(BaseModel):
    response: GetBanned = None


GetById = typing.List[objects.groups.GroupFull]


class GetByIdModel(BaseModel):
    response: GetById = None


class GetCallbackConfirmationCode(BaseModel):
    code: str = None


class GetCallbackConfirmationCodeModel(BaseModel):
    response: GetCallbackConfirmationCode = None


class GetCallbackServers(BaseModel):
    count: int = None
    items: typing.List[objects.groups.CallbackServer] = None


class GetCallbackServersModel(BaseModel):
    response: GetCallbackServers = None


GetCallbackSettings = objects.groups.CallbackSettings


class GetCallbackSettingsModel(BaseModel):
    response: GetCallbackSettings = None


class Category(BaseModel):
    id: int = None
    name: str = None


class GetCatalogInfo(BaseModel):
    enabled: int = None
    categories: typing.List[Category] = None
    page_count: int = None
    page_previews: typing.List[objects.groups.Group] = None


class GetCatalogInfoModel(BaseModel):
    response: GetCatalogInfo = None


class GetCatalog(BaseModel):
    count: int = None
    items: typing.List[objects.groups.Group] = None


class GetCatalogModel(BaseModel):
    response: GetCatalog = None


class GetInvitedUsers(BaseModel):
    count: int = None
    items: typing.List[objects.users.User] = None


class GetInvitedUsersModel(BaseModel):
    response: GetInvitedUsers = None


class GetInvites(BaseModel):
    count: int = None
    items: typing.List[objects.groups.Group] = None


class GetInvitesModel(BaseModel):
    response: GetInvites = None


GetLongPollServer = objects.groups.LongPollServer


class GetLongPollServerModel(BaseModel):
    response: GetLongPollServer = None


GetLongPollSettings = objects.groups.LongPollSettings


class GetLongPollSettingsModel(BaseModel):
    response: GetLongPollSettings = None


class GetMembers(BaseModel):
    count: int = None
    items: typing.List[typing.Union[int, objects.users.User]] = None


class GetMembersModel(BaseModel):
    response: GetMembers = None


class GetRequests(BaseModel):
    count: int = None
    items: typing.List[typing.Union[int, objects.users.User]] = None


class GetRequestsModel(BaseModel):
    response: GetRequests = None


GetSettings = objects.groups.GroupSettings


class GetSettingsModel(BaseModel):
    response: GetSettings = None


class Setting(BaseModel):
    setting: int = None
    name: str = None


class GetTokenPermissions(BaseModel):
    mask: int = None
    settings: typing.List[Setting] = None


class GetTokenPermissionsModel(BaseModel):
    response: GetTokenPermissions = None


class Get(BaseModel):
    count: int = None
    items: typing.List[typing.Union[int, objects.groups.Group]] = None


class GetModel(BaseModel):
    response: Get = None


IsMember = objects.base.BoolInt


class IsMemberModel(BaseModel):
    response: IsMember = None
