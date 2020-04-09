from . import base
import typing
from enum import Enum
from ..base import BaseModel
from vkbottle.types import objects


class PrivacySettings(Enum):
    _0 = "0"
    _1 = "1"
    _2 = "2"


class Wikipage(BaseModel):
    creator_id: int = None
    creator_name: int = None
    editor_id: int = None
    editor_name: str = None
    group_id: int = None
    id: int = None
    title: str = None
    views: int = None
    who_can_edit: "PrivacySettings" = None
    who_can_view: "PrivacySettings" = None


class WikipageFull(BaseModel):
    created: int = None
    creator_id: int = None
    current_user_can_edit: "base.BoolInt" = None
    current_user_can_edit_access: "base.BoolInt" = None
    edited: int = None
    editor_id: int = None
    group_id: int = None
    html: str = None
    id: int = None
    source: str = None
    title: str = None
    view_url: str = None
    views: int = None
    who_can_edit: "PrivacySettings" = None
    who_can_view: "PrivacySettings" = None


class WikipageHistory(BaseModel):
    id: int = None
    length: int = None
    date: int = None
    editor_id: int = None
    editor_name: str = None


Wikipage.update_forward_refs()
WikipageFull.update_forward_refs()
WikipageHistory.update_forward_refs()
