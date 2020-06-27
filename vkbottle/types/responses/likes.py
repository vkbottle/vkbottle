import typing
from ..base import BaseModel
from vkbottle.types import objects


class IsLiked(BaseModel):
    liked: objects.base.BoolInt = None
    copied: objects.base.BoolInt = None


class IsLikedModel(BaseModel):
    response: IsLiked = None


class Add(BaseModel):
    likes: int = None


class AddModel(BaseModel):
    response: Add = None


class Delete(BaseModel):
    likes: int = None


class DeleteModel(BaseModel):
    response: Delete = None


class GetList(BaseModel):
    count: int = None
    items: typing.List[int] = None


class GetListModel(BaseModel):
    response: GetList = None
