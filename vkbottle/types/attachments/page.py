from ..base import BaseModel

# https://vk.com/dev/objects/page


class Page(BaseModel):
    id: int = None
    group_id: int = None
    creator_id: int = None
    title: str = None
    current_user_can_edit: int = None
    current_user_can_edit_access: int = None
    who_can_view: int = None
    who_can_edit: int = None
    edited: int = None
    created: int = None
    editor_id: int = None
    views: int = None
    parent: str = None
    parent2: str = None
    source: str = None
    html: str = None
    view_url: str = None
