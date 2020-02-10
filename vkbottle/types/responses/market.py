from .others import SimpleResponse
from ..base import BaseModel

from ..attachments.market import (
    Market,
    MarketCategorySection,
    MarketPrice,
    MarketCategory,
)
from ..attachments.market_album import MarketAlbum
from ..user import User
from ..attachments import Attachments
from ..attachments import Photo


from typing import List, Dict, Any


class AddResponse(BaseModel):
    market_item_id: int = None


class Add(BaseModel):
    response: AddResponse = None


class AddAlbumResponse(BaseModel):
    market_album_id: int = None


class AddAlbum(BaseModel):
    response: AddAlbumResponse = None


class AddToAlbum(SimpleResponse):
    pass


class CreateComment(SimpleResponse):
    pass


class Delete(SimpleResponse):
    pass


class DeleteAlbum(SimpleResponse):
    pass


class DeleteComment(SimpleResponse):
    pass


class Edit(SimpleResponse):
    pass


class EditAlbum(SimpleResponse):
    pass


class EditComment(SimpleResponse):
    pass


class GetResponse(BaseModel):
    count: int = None
    items: List[Market] = []


class Get(BaseModel):
    response: GetResponse = None


class GetAlbumByIdResponse(BaseModel):
    count: int = None
    items: List[MarketAlbum] = []


class GetAlbumById(BaseModel):
    response: GetAlbumByIdResponse = None


class GetAlbums(BaseModel):
    response: GetAlbumByIdResponse = None


class GetById(BaseModel):
    response: GetResponse = None


class GetCategoriesResponseItem(BaseModel):
    id: int = None
    name: str = None
    section: MarketCategorySection = None


class GetCategoriesResponse(BaseModel):
    count: int = None
    items: List[GetCategoriesResponseItem] = []


class GetCommentsResponse(BaseModel):
    count: int = None
    items: List[Dict] = []
    attachment: List[Attachments] = []
    profiles: List[User] = []


class GetComments(BaseModel):
    response: GetCommentsResponse = None


class RemoveFromAlbum(SimpleResponse):
    pass


class ReorderAlbums(SimpleResponse):
    pass


class ReorderItems(SimpleResponse):
    pass


class Report(SimpleResponse):
    pass


class ReportComment(SimpleResponse):
    pass


class Restore(SimpleResponse):
    pass


class RestoreComment(SimpleResponse):
    pass


class SearchResponse(BaseModel):
    count: int = None
    items: List[Any] = []
    date: int = None
    description: str = None
    external_id: str = None
    id: int = None
    owner_id: int = None
    price: MarketPrice = None
    thumb_photo: str = None
    title: str = None
    albums_ids: List[int] = []
    photos: List[Photo] = None
    can_comment: int = None
    can_repost: int = None
    likes: dict = {}
    reposts: dict = {}
    views_count: int = None


class Search(BaseModel):
    response: SearchResponse = None
