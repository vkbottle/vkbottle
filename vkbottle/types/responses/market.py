import typing
from ..base import BaseModel
from vkbottle.types import objects


class Search(BaseModel):
    count: int = None
    items: typing.List[objects.market.MarketItem] = None


class SearchModel(BaseModel):
    response: Search = None


class AddAlbum(BaseModel):
    market_album_id: int = None


class AddAlbumModel(BaseModel):
    response: AddAlbum = None


class Add(BaseModel):
    market_item_id: int = None


class AddModel(BaseModel):
    response: Add = None


CreateComment = typing.Dict


class CreateCommentModel(BaseModel):
    response: CreateComment = None


DeleteComment = objects.base.BoolInt


class DeleteCommentModel(BaseModel):
    response: DeleteComment = None


class GetAlbumById(BaseModel):
    count: int = None
    items: typing.List[objects.market.MarketAlbum] = None


class GetAlbumByIdModel(BaseModel):
    response: GetAlbumById = None


class GetAlbums(BaseModel):
    count: int = None
    items: typing.List[objects.market.MarketAlbum] = None


class GetAlbumsModel(BaseModel):
    response: GetAlbums = None


class GetById(BaseModel):
    count: int = None
    items: typing.List[objects.market.MarketItem] = None


class GetByIdModel(BaseModel):
    response: GetById = None


class GetCategories(BaseModel):
    count: int = None
    items: typing.List[objects.market.MarketCategory] = None


class GetCategoriesModel(BaseModel):
    response: GetCategories = None


class GetComments(BaseModel):
    count: int = None
    items: typing.List[objects.wall.WallComment] = None
    profiles: typing.List[objects.users.User] = None


class GetCommentsModel(BaseModel):
    response: GetComments = None


class Get(BaseModel):
    count: int = None
    items: typing.List[objects.market.MarketItem] = None


class GetModel(BaseModel):
    response: Get = None


RestoreComment = objects.base.BoolInt


class RestoreCommentModel(BaseModel):
    response: RestoreComment = None
