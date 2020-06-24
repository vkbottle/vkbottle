from . import base
from enum import Enum
from ..base import BaseModel


class Wikipage(BaseModel):
    creator_id: int = None
    creator_name: int = None
    editor_id: int = None
    editor_name: str = None
    group_id: int = None
    id: int = None
    title: str = None
    views: int = None
    who_can_edit: int = None
    who_can_view: int = None

    def __hash__(self):
        return hash((self.group_id, self.id))

    def __eq__(self, other):
        return self.group_id == other.group_id and self.id == other.id


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
    who_can_edit: int = None
    who_can_view: int = None

    def __hash__(self):
        return hash((self.group_id, self.id))

    def __eq__(self, other):
        return self.group_id == other.group_id and self.id == other.id


class WikipageHistory(BaseModel):
    id: int = None
    length: int = None
    date: int = None
    editor_id: int = None
    editor_name: str = None


Wikipage.update_forward_refs()
WikipageFull.update_forward_refs()
WikipageHistory.update_forward_refs()
