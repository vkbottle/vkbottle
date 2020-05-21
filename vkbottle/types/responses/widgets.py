import typing
from ..base import BaseModel
from vkbottle.types import objects


class GetPages(BaseModel):
    count: int = None
    pages: typing.List[objects.widgets.WidgetPage] = None


class GetPagesModel(BaseModel):
    response: GetPages = None


class GetComments(BaseModel):
    count: int = None
    posts: typing.List[objects.widgets.WidgetComment] = None


class GetCommentsModel(BaseModel):
    response: GetComments = None
