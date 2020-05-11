from . import base, users, wall
import typing
from enum import Enum
from ..base import BaseModel


class CommentMedia(BaseModel):
    item_id: int = None
    owner_id: int = None
    thumb_src: str = None
    type: "CommentMediaType" = None


class CommentMediaType(Enum):
    audio = "audio"
    photo = "photo"
    video = "video"


class CommentReplies(BaseModel):
    can_post: "base.BoolInt" = None
    count: int = None
    replies: typing.List = None


class CommentRepliesItem(BaseModel):
    cid: int = None
    date: int = None
    likes: "WidgetLikes" = None
    text: str = None
    uid: int = None
    user: "users.UserFull" = None


class WidgetComment(BaseModel):
    attachments: typing.List = None
    can_delete: "base.BoolInt" = None
    comments: "CommentReplies" = None
    date: int = None
    from_id: int = None
    id: int = None
    likes: "base.LikesInfo" = None
    media: "CommentMedia" = None
    post_source: "wall.PostSource" = None
    post_type: int = None
    reposts: "base.RepostsInfo" = None
    text: str = None
    to_id: int = None
    user: "users.UserFull" = None


class WidgetLikes(BaseModel):
    count: int = None


class WidgetPage(BaseModel):
    comments: "base.ObjectCount" = None
    date: int = None
    description: str = None
    id: int = None
    likes: "base.ObjectCount" = None
    page_id: str = None
    photo: str = None
    title: str = None
    url: str = None


CommentMedia.update_forward_refs()
CommentReplies.update_forward_refs()
CommentRepliesItem.update_forward_refs()
WidgetComment.update_forward_refs()
WidgetLikes.update_forward_refs()
WidgetPage.update_forward_refs()
