import typing
from ..base import BaseModel
from vkbottle.types import objects


class Search(BaseModel):
    count: int = None
    items: typing.List[objects.video.Video] = None


class SearchModel(BaseModel):
    response: Search = None


class AddAlbum(BaseModel):
    album_id: int = None


class AddAlbumModel(BaseModel):
    response: AddAlbum = None


CreateComment = typing.Dict


class CreateCommentModel(BaseModel):
    response: CreateComment = None


GetAlbumById = objects.video.VideoAlbumFull


class GetAlbumByIdModel(BaseModel):
    response: GetAlbumById = None


GetAlbumsByVideo = typing.List[int]


class GetAlbumsByVideoModel(BaseModel):
    response: GetAlbumsByVideo = None


class GetAlbums(BaseModel):
    count: int = None
    items: typing.List[objects.video.VideoAlbumFull] = None


class GetAlbumsModel(BaseModel):
    response: GetAlbums = None


class GetComments(BaseModel):
    count: int = None
    items: typing.List[objects.wall.WallComment] = None


class GetCommentsModel(BaseModel):
    response: GetComments = None


class Get(BaseModel):
    count: int = None
    items: typing.List[objects.video.Video] = None


class GetModel(BaseModel):
    response: Get = None


RestoreComment = objects.base.BoolInt


class RestoreCommentModel(BaseModel):
    response: RestoreComment = None


Save = objects.video.SaveResult


class SaveModel(BaseModel):
    response: Save = None
