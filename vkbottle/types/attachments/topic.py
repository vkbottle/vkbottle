from ..base import BaseModel
from .like import Like
from .attachments import Attachments

# https://vk.com/dev/objects/topic
# https://vk.com/dev/objects/comment_board


class TopicComment(BaseModel):
    id: int = None
    from_id: int = None
    date: int = None
    text: str = None
    attachments: Attachments = None
    likes: Like = None


class Topic(BaseModel):
    id: int = None
    title: str = None
    created: int = None
    created_by: int = None
    updated: int = None
    updated_by: int = None
    is_closed: int = None
    is_fixed: int = None
    comments: int = None
    first_comment: str = None
    last_comment: str = None
