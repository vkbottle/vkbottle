import typing
from ..base import BaseModel
from vkbottle.types import objects

SendNotification = typing.List[int]


class SendNotificationModel(BaseModel):
    response: SendNotification = None


CheckToken = objects.secure.TokenChecked


class CheckTokenModel(BaseModel):
    response: CheckToken = None


GetAppBalance = typing.Dict


class GetAppBalanceModel(BaseModel):
    response: GetAppBalance = None


GetSMSHistory = typing.List[objects.secure.SmsNotification]


class GetSMSHistoryModel(BaseModel):
    response: GetSMSHistory = None


GetTransactionsHistory = typing.List[objects.secure.Transaction]


class GetTransactionsHistoryModel(BaseModel):
    response: GetTransactionsHistory = None


GetUserLevel = typing.List[objects.secure.Level]


class GetUserLevelModel(BaseModel):
    response: GetUserLevel = None


GiveEventSticker = typing.List[typing.Dict]


class GiveEventStickerModel(BaseModel):
    response: GiveEventSticker = None
