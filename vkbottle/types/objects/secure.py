from . import base
from ..base import BaseModel


class Level(BaseModel):
    level: int = None
    uid: int = None


class SmsNotification(BaseModel):
    app_id: str = None
    date: str = None
    id: str = None
    message: str = None
    user_id: str = None


class TokenChecked(BaseModel):
    date: int = None
    expire: int = None
    success: "base.OkResponse" = None
    user_id: int = None


class Transaction(BaseModel):
    date: int = None
    id: int = None
    uid_from: int = None
    uid_to: int = None
    votes: int = None


Level.update_forward_refs()
SmsNotification.update_forward_refs()
TokenChecked.update_forward_refs()
Transaction.update_forward_refs()
