from .base import BaseModel
from .attachments import Attachments

import typing


# https://vk.com/dev/objects/comment


class WallCommentThread(BaseModel):
    count: int = None
    items: typing.List["WallComment"] = None
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
    attachments: Attachments = None
    parents_stack: typing.List[int] = None
    thread: WallCommentThread = None


WallCommentThread.update_forward_refs()
