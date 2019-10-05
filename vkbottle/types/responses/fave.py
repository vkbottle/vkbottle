from .others import SimpleResponse
from ..base import BaseModel

import typing


class AddArticle(SimpleResponse):
    pass


class AddLink(SimpleResponse):
    pass


class AddPage(SimpleResponse):
    pass


class AddPost(SimpleResponse):
    pass


class AddProduct(SimpleResponse):
    pass


class AddTagResponse(BaseModel):
    id: int = None
    name: str = None


class AddTag(BaseModel):
    response: AddTagResponse = None


class AddVideo(SimpleResponse):
    pass


class EditTag(SimpleResponse):
    pass


class Get(BaseModel):
    response: typing.Any = None


class GetPages(BaseModel):
    response: typing.Any = None


class GetTagsResponse(BaseModel):
    count: int = None
    items: typing.List[AddTagResponse] = None


class GetTags(BaseModel):
    response: GetTagsResponse = None


class MarkSeen(SimpleResponse):
    pass


class RemoveArticle(SimpleResponse):
    pass


class RemoveLink(SimpleResponse):
    pass


class RemovePage(SimpleResponse):
    pass


class RemovePost(SimpleResponse):
    pass


class RemoveProduct(SimpleResponse):
    pass


class RemoveTag(SimpleResponse):
    pass


class RemoveVideo(SimpleResponse):
    pass


class ReorderTags(SimpleResponse):
    pass


class SetPageTags(SimpleResponse):
    pass


class SetTags(SimpleResponse):
    pass


class TrackPageInteraction(SimpleResponse):
    pass
