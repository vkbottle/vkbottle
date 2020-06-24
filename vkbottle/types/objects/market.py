from . import photos, base
import typing
from ..base import BaseModel


class Currency(BaseModel):
    id: int = None
    name: str = None


class MarketAlbum(BaseModel):
    count: int = None
    id: int = None
    owner_id: int = None
    photo: "photos.Photo" = None
    title: str = None
    updated_time: int = None

    def __hash__(self):
        return hash((self.owner_id, self.id))

    def __eq__(self, other):
        return self.owner_id == other.owner_id and self.id == other.id


class MarketCategory(BaseModel):
    id: int = None
    name: str = None
    section: "Section" = None


class MarketItem(BaseModel):
    access_key: str = None
    availability: int = None
    button_title: str = None
    category: "MarketCategory" = None
    date: int = None
    description: str = None
    external_id: str = None
    id: int = None
    is_favorite: bool = None
    owner_id: int = None
    price: "Price" = None
    thumb_photo: str = None
    title: str = None
    url: str = None

    def __hash__(self):
        return hash((self.owner_id, self.id))

    def __eq__(self, other):
        return self.owner_id == other.owner_id and self.id == other.id


class MarketItemFull(MarketItem):
    albums_ids: typing.List = None
    photos: typing.List = None
    can_comment: "base.BoolInt" = None
    can_repost: "base.BoolInt" = None
    likes: "base.Likes" = None
    reposts: "base.RepostsInfo" = None
    views_count: int = None


class Price(BaseModel):
    amount: str = None
    currency: "Currency" = None
    discount_rate: int = None
    old_amount: str = None
    text: str = None


class Section(BaseModel):
    id: int = None
    name: str = None


Currency.update_forward_refs()
MarketAlbum.update_forward_refs()
MarketCategory.update_forward_refs()
MarketItem.update_forward_refs()
MarketItemFull.update_forward_refs()
Price.update_forward_refs()
Section.update_forward_refs()
