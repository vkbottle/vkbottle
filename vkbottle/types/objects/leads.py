from . import base
from enum import Enum
from ..base import BaseModel


class Checked(BaseModel):
    reason: str = None
    result: "CheckedResult" = None
    sid: str = None
    start_link: str = None


class CheckedResult(Enum):
    true = "true"
    false = "false"


class Complete(BaseModel):
    cost: int = None
    limit: int = None
    spent: int = None
    success: "base.OkResponse" = None
    test_mode: "base.BoolInt" = None


class Entry(BaseModel):
    aid: int = None
    comment: str = None
    date: int = None
    sid: str = None
    start_date: int = None
    status: int = None
    test_mode: "base.BoolInt" = None
    uid: int = None


class Lead(BaseModel):
    completed: int = None
    cost: int = None
    days: "LeadDays" = None
    impressions: int = None
    limit: int = None
    spent: int = None
    started: int = None


class LeadDays(BaseModel):
    completed: int = None
    impressions: int = None
    spent: int = None
    started: int = None


class Start(BaseModel):
    test_mode: "base.BoolInt" = None
    vk_sid: str = None


Checked.update_forward_refs()
Complete.update_forward_refs()
Entry.update_forward_refs()
Lead.update_forward_refs()
LeadDays.update_forward_refs()
Start.update_forward_refs()
