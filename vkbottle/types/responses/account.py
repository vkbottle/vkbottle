from .others import SimpleResponse
from ..base import BaseModel

from ..additional import ActiveOffer, Sex, BdateVisiblity, Country, City, NameRequest
from ..user import User, UserRelation
from ..community import Community

import typing


class Ban(SimpleResponse):
    pass


class ChangePasswordResponse(BaseModel):
    token: str = None
    secret: str = None


class ChangePassword(BaseModel):
    response: ChangePasswordResponse = None


class GetActiveOffersResponse(BaseModel):
    count: int = None
    items: typing.List[ActiveOffer] = []


class GetActiveOffers(BaseModel):
    response: GetActiveOffersResponse = None


class GetAppPermissions(SimpleResponse):
    pass


class GetBannedResponse(BaseModel):
    count: int = None
    items: typing.List[int] = None
    profiles: typing.List[User] = None
    groups: typing.List[Community] = None


class GetBanned(BaseModel):
    response: GetBannedResponse = None


class GetCountersResponse(BaseModel):
    friends: int = None
    friends_suggestions: int = None
    messages: int = None
    photos: int = None
    videos: int = None
    gifts: int = None
    events: int = None
    groups: int = None
    sdk: int = None
    app_requests: int = None


class GetCounters(BaseModel):
    response: GetCountersResponse = None


class GetInfoResponse(BaseModel):
    country: str = None
    https_required: int = None
    _2fa_required: int = None
    own_posts_default: int = None
    no_wall_replies: int = None
    intro: int = None
    lang: int = None


class GetInfo(BaseModel):
    response: GetInfoResponse = None


class GetProfileInfoResponse(BaseModel):
    first_name: str = None
    last_name: str = None
    maiden_name: str = None
    screen_name: str = None
    sex: Sex = None
    relation: UserRelation = None
    relation_partner: User = None
    relation_pending: int = None
    relation_requests: typing.List[User] = None
    bdate: str = None
    bdate_visiblity: BdateVisiblity = None
    home_town: str = None
    country: Country = None
    city: City = None
    name_request: NameRequest = None
    status: str = None
    phone: str = None


class GetProfileInfo(BaseModel):
    response: GetProfileInfoResponse = None


class GetPushSettingsResponse(BaseModel):
    disabled: int = None
    disabled_until: int = None
    conversations: list = None
    settings: typing.Any = None


class GetPushSettings(BaseModel):
    response: GetPushSettingsResponse = None


class RegisterDevice(SimpleResponse):
    pass


class SaveProfileInfoResponse(BaseModel):
    changed: int = None
    name_request: NameRequest = None


class SaveProfileInfo(BaseModel):
    response: SaveProfileInfoResponse = None


class SetInfo(SimpleResponse):
    pass


class SetNameInMenu(SimpleResponse):
    pass


class SetOffline(SimpleResponse):
    pass


class SetOnline(SimpleResponse):
    pass


class SetPushSettings(SimpleResponse):
    pass


class SetSilenceMode(SimpleResponse):
    pass


class Unban(SimpleResponse):
    pass


class UnregisterDevice(SimpleResponse):
    pass
