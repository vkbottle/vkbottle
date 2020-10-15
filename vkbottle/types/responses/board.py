import typing
from ..base import BaseModel
from vkbottle.types import objects


class GetTopics(BaseModel):
    count: int = None
    items: typing.List[objects.board.Topic] = None
    default_order: int = None
    can_add_topics: objects.base.BoolInt = None
    profiles: typing.List[objects.users.UserFull]


class GetTopicsModel(BaseModel):
    response: GetTopics = None


AddTopic = int


class AddTopicModel(BaseModel):
    response: AddTopic = None


CreateComment = int


class CreateCommentModel(BaseModel):
    response: CreateComment = None


class GetComments(BaseModel):
    count: int = None
    items: typing.List[objects.board.TopicComment] = None
    poll: objects.board.TopicPoll = None


class GetCommentsModel(BaseModel):
    response: GetComments = None
