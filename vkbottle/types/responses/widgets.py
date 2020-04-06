import typing
import enum
from ..base import BaseModel
from vkbottle.types import objects


class GetPages(BaseModel):
    count: int = None
    pages: typing.List = None


class GetPagesModel(BaseModel):
    response: GetPages = None


class GetComments(BaseModel):
    count: int = None
    posts: typing.List = None


class GetCommentsModel(BaseModel):
    response: GetComments = None
