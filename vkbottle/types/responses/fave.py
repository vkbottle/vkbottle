import typing
from ..base import BaseModel
from vkbottle.types import objects


class Fave(BaseModel):
    added_date: int = None
    seen: bool = None
    type: str = None
    link: objects.link.Link = None
    tags: typing.List[str] = None


class Get(BaseModel):
    count: int = None
    items: typing.List[Fave] = None


class GetModel(BaseModel):
    response: Get = None


AddTag = objects.fave.Tag


class AddTagModel(BaseModel):
    response: AddTag = None


class GetPages(BaseModel):
    count: int = None
    items: typing.List[objects.fave.Page] = None


class GetPagesModel(BaseModel):
    response: GetPages = None


class GetTags(BaseModel):
    count: int = None
    items: typing.List[objects.fave.Tag] = None


class GetTagsModel(BaseModel):
    response: GetTags = None
