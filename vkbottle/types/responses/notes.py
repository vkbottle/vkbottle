import typing
from ..base import BaseModel
from vkbottle.types import objects


class Get(BaseModel):
    count: int = None
    items: typing.List = None


class GetModel(BaseModel):
    response: Get = None


Add = typing.Dict


class AddModel(BaseModel):
    response: Add = None


CreateComment = typing.Dict


class CreateCommentModel(BaseModel):
    response: CreateComment = None


GetById = objects.notes.Note


class GetByIdModel(BaseModel):
    response: GetById = None


class GetComments(BaseModel):
    count: int = None
    items: typing.List = None


class GetCommentsModel(BaseModel):
    response: GetComments = None
