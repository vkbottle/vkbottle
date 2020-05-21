import typing
from ..base import BaseModel
from vkbottle.types import objects


class Search(BaseModel):
    count: int = None
    items: typing.List[objects.photos.Photo] = None


class SearchModel(BaseModel):
    response: Search = None


Copy = typing.Dict


class CopyModel(BaseModel):
    response: Copy = None


CreateAlbum = objects.photos.PhotoAlbumFull


class CreateAlbumModel(BaseModel):
    response: CreateAlbum = None


CreateComment = typing.Dict


class CreateCommentModel(BaseModel):
    response: CreateComment = None


DeleteComment = objects.base.BoolInt


class DeleteCommentModel(BaseModel):
    response: DeleteComment = None


GetAlbumsCount = typing.Dict


class GetAlbumsCountModel(BaseModel):
    response: GetAlbumsCount = None


class GetAlbums(BaseModel):
    count: int = None
    items: typing.List[objects.photos.PhotoAlbum] = None


class GetAlbumsModel(BaseModel):
    response: GetAlbums = None


class GetAllComments(BaseModel):
    count: int = None
    items: typing.List[objects.photos.CommentXtrPid] = None


class GetAllCommentsModel(BaseModel):
    response: GetAllComments = None


class GetAll(BaseModel):
    count: int = None
    items: typing.List[objects.photos.Photo] = None
    more: objects.base.BoolInt = None


class GetAllModel(BaseModel):
    response: GetAll = None


GetById = typing.List[objects.photos.Photo]


class GetByIdModel(BaseModel):
    response: GetById = None


class GetComments(BaseModel):
    count: int = None
    real_offset: int = None
    items: typing.List[objects.photos.CommentXtrPid] = None


class GetCommentsModel(BaseModel):
    response: GetComments = None


GetMarketUploadServer = objects.base.UploadServer


class GetMarketUploadServerModel(BaseModel):
    response: GetMarketUploadServer = None


GetMessagesUploadServer = objects.photos.PhotoUpload


class GetMessagesUploadServerModel(BaseModel):
    response: GetMessagesUploadServer = None


class GetNewTags(BaseModel):
    count: int = None
    items: typing.List[objects.photos.PhotoTag] = None


class GetNewTagsModel(BaseModel):
    response: GetNewTags = None


GetTags = typing.List[objects.photos.PhotoTag]


class GetTagsModel(BaseModel):
    response: GetTags = None


GetUploadServer = objects.photos.PhotoUpload


class GetUploadServerModel(BaseModel):
    response: GetUploadServer = None


class GetUserPhotos(BaseModel):
    count: int = None
    items: typing.List[objects.photos.Photo] = None


class GetUserPhotosModel(BaseModel):
    response: GetUserPhotos = None


GetWallUploadServer = objects.photos.PhotoUpload


class GetWallUploadServerModel(BaseModel):
    response: GetWallUploadServer = None


class Get(BaseModel):
    count: int = None
    items: typing.List[objects.photos.Photo] = None


class GetModel(BaseModel):
    response: Get = None


PutTag = typing.Dict


class PutTagModel(BaseModel):
    response: PutTag = None


RestoreComment = objects.base.BoolInt


class RestoreCommentModel(BaseModel):
    response: RestoreComment = None


SaveMarketAlbumPhoto = typing.List[objects.photos.Photo]


class SaveMarketAlbumPhotoModel(BaseModel):
    response: SaveMarketAlbumPhoto = None


SaveMarketPhoto = typing.List[objects.photos.Photo]


class SaveMarketPhotoModel(BaseModel):
    response: SaveMarketPhoto = None


SaveMessagesPhoto = typing.List[objects.photos.Photo]


class SaveMessagesPhotoModel(BaseModel):
    response: SaveMessagesPhoto = None


SaveOwnerCoverPhoto = typing.List[objects.base.Image]


class SaveOwnerCoverPhotoModel(BaseModel):
    response: SaveOwnerCoverPhoto = None


class SaveOwnerPhoto(BaseModel):
    photo_hash: str = None
    photo_src: str = None
    photo_src_big: str = None
    photo_src_small: str = None
    saved: int = None
    post_id: int = None


class SaveOwnerPhotoModel(BaseModel):
    response: SaveOwnerPhoto = None


SaveWallPhoto = typing.List[objects.photos.Photo]


class SaveWallPhotoModel(BaseModel):
    response: SaveWallPhoto = None


Save = typing.List[objects.photos.Photo]


class SaveModel(BaseModel):
    response: Save = None
