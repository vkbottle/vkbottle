import typing
from ..base import BaseModel


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
