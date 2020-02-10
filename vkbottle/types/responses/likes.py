from .others import SimpleResponse
from ..base import BaseModel

from typing import List


class AddResponse(BaseModel):
    likes: int = None


class Add(BaseModel):
    response: AddResponse = None


class Delete(BaseModel):
    response: AddResponse = None


class GetListResponse(BaseModel):
    count: int = None
    items: List[int] = []


class GetList(BaseModel):
    response: GetListResponse = None


class IsLikedResponse(BaseModel):
    liked: int = None
    copied: int = None


class IsLiked(BaseModel):
    response: IsLikedResponse = None
