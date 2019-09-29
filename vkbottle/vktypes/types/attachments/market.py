from ..base import BaseModel
from ..attachments import Photo, Like

import typing


# https://vk.com/dev/objects/market_item


class MarketPriceCurrency(BaseModel):
    id: int = None
    name: str = None


class MarketPrice(BaseModel):
    amount: int = None
    currency: MarketPriceCurrency = None
    text: str = None


class MarketCategorySection(BaseModel):
    id: int = None
    name: str = None


class MarketCategory(BaseModel):
    id: int = None
    name: str = None
    section: MarketCategorySection = None


class Market(BaseModel):
    id: int = None
    owner_id: int = None
    title: str = None
    description: str = None
    price: MarketPrice = None
    category: MarketCategory = None
    thumb_photo: str = None
    date: int = None
    availability: int = None
    is_favorite: bool = None
    photos: typing.List[Photo] = None
    can_comment: int = None
    can_repost: int = None
    likes: Like = None
    url: str = None
    button_title: str = None
