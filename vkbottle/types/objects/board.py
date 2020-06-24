from . import base
import typing
from ..base import BaseModel


class Topic(BaseModel):
    comments: int = None
    created: int = None
    created_by: int = None
    id: int = None
    is_closed: "base.BoolInt" = None
    is_fixed: "base.BoolInt" = None
    title: str = None
    updated: int = None
    updated_by: int = None

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return self.id == other.id


class TopicComment(BaseModel):
    attachments: typing.List = None
    date: int = None
    from_id: int = None
    id: int = None
    real_offset: int = None
    text: str = None


class TopicPoll(BaseModel):
    answer_id: int = None
    answers: typing.List = None
    created: int = None
    is_closed: "base.BoolInt" = None
    owner_id: int = None
    poll_id: int = None
    question: str = None
    votes: str = None


Topic.update_forward_refs()
TopicComment.update_forward_refs()
TopicPoll.update_forward_refs()
