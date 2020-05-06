import typing
from ..base import BaseModel


class ChatPreview(BaseModel):
    admin_id: int = None
    joined: bool = None
    local_id: int = None
    members: typing.List = None
    members_count: int = None
    title: str = None


ChatPreview.update_forward_refs()
