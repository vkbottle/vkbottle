from .others import SimpleResponse
from ..base import BaseModel

from ..attachments.topic import TopicComment, Topic
from ..user import User

import typing


class AddTopic(SimpleResponse):
    pass


class CloseTopic(SimpleResponse):
    pass


class CreateComment(SimpleResponse):
    pass


class DeleteComment(SimpleResponse):
    pass


class DeleteTopic(SimpleResponse):
    pass


class EditComment(SimpleResponse):
    pass


class EditTopic(SimpleResponse):
    pass


class FixTopic(SimpleResponse):
    pass


class GetCommentsResponse(BaseModel):
    count: int = None
    items: typing.List[TopicComment] = None
    profiles: typing.List[User] = None


class GetComments(BaseModel):
    response: GetCommentsResponse = None


class GetTopicsResponse(BaseModel):
    count: int = None
    items: typing.List[Topic] = None
    default_order: int = None
    can_add_topics: int = None
    profiles: typing.List[User] = None


class GetTopics(BaseModel):
    response: GetTopicsResponse = None


class OpenTopic(SimpleResponse):
    pass


class RestoreComment(SimpleResponse):
    pass


class UnfixTopic(SimpleResponse):
    pass
