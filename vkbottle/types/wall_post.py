from .base import BaseModel
from .attachments import Like, Repost, Geo, Attachment

from .additional import PostSource
import typing

# https://vk.com/dev/objects/post


class WallPostComments(BaseModel):
    count: int = None
    can_post: int = None
    groups_can_post: int = None


class WallPost(BaseModel):
    id: int = None
    owner_id: int = None
    from_id: int = None
    created_by: int = None
    date: int = None
    text: str = None
    reply_owner_id: int = None
    reply_post_id: int = None
    friends_only: int = None
    comments: WallPostComments = None
    likes: Like = None
    reposts: Repost = None
    post_type: str = None
    post_source: PostSource = None
    attachments: typing.List[Attachment] = None
    geo: Geo = None
    signer_id: int = None
    copy_history: typing.Any = None
    can_pin: int = None
    can_delete: int = None
    can_edit: int = None
    is_pinned: int = None
    marked_as_ads: int = None
    is_favorite: bool = None
