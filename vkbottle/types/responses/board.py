import typing
from ..base import BaseModel
from vkbottle.types import objects


class GetTopics(BaseModel):
    count: int = None
    items: typing.List[objects.board.Topic] = None
    can_add_topics: objects.base.BoolInt = None


class GetTopicsModel(BaseModel):
    response: GetTopics = None


AddTopic = typing.Dict


class AddTopicModel(BaseModel):
    response: AddTopic = None


CreateComment = typing.Dict


class CreateCommentModel(BaseModel):
    response: CreateComment = None


class GetComments(BaseModel):
    count: int = None
    items: typing.List[objects.board.TopicComment] = None
    poll: objects.board.TopicPoll = None


class GetCommentsModel(BaseModel):
    response: GetComments = None
