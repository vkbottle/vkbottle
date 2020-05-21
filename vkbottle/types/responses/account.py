import typing
from ..base import BaseModel
from vkbottle.types import objects


class SaveProfileInfo(BaseModel):
    changed: objects.base.BoolInt = None
    name_request: objects.account.NameRequest = None


class SaveProfileInfoModel(BaseModel):
    response: SaveProfileInfo = None


class ChangePassword(BaseModel):
    token: str = None
    secret: str = None


class ChangePasswordModel(BaseModel):
    response: ChangePassword = None


class GetActiveOffers(BaseModel):
    count: int = None
    items: typing.List[int] = None


class GetActiveOffersModel(BaseModel):
    response: GetActiveOffers = None


GetAppPermissions = typing.Dict


class GetAppPermissionsModel(BaseModel):
    response: GetAppPermissions = None


class GetBanned(BaseModel):
    count: int = None
    items: typing.List[objects.users.User] = None


class GetBannedModel(BaseModel):
    response: GetBanned = None


GetCounters = objects.account.AccountCounters


class GetCountersModel(BaseModel):
    response: GetCounters = None


GetInfo = objects.account.Info


class GetInfoModel(BaseModel):
    response: GetInfo = None


GetProfileInfo = objects.account.UserSettingsInterest


class GetProfileInfoModel(BaseModel):
    response: GetProfileInfo = None


GetPushSettings = objects.account.PushSettings


class GetPushSettingsModel(BaseModel):
    response: GetPushSettings = None
