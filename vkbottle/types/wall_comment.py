from .base import BaseModel
from .attachments.attachments_w import AttachmentW

from typing import List


# https://vk.com/dev/objects/comment


class WallCommentThread(BaseModel):
    count: int = None
    items: List["WallComment"] = []
    can_post: bool = None
    show_reply_button: bool = None
    groups_can_post: bool = None


class WallComment(BaseModel):
    id: int = None
    from_id: int = None
    date: int = None
    text: str = None
    reply_to_user: int = None
    reply_to_comment: int = None
    attachments: List[AttachmentW] = []
    parents_stack: List[int] = []
    thread: WallCommentThread = None
    post_id: int = None
    owner_id: int = None


WallCommentThread.update_forward_refs()
