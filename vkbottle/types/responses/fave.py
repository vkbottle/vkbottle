import typing
from ..base import BaseModel
from vkbottle.types import objects


class Get(BaseModel):
    count: int = None
    items: typing.List = None


class GetModel(BaseModel):
    response: Get = None


AddTag = objects.fave.Tag


class AddTagModel(BaseModel):
    response: AddTag = None


class GetPages(BaseModel):
    count: int = None
    items: typing.List = None


class GetPagesModel(BaseModel):
    response: GetPages = None


class GetTags(BaseModel):
    count: int = None
    items: typing.List = None


class GetTagsModel(BaseModel):
    response: GetTags = None
