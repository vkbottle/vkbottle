from ..base import BaseModel
from enum import Enum
from . import market, photos


class Link(BaseModel):
    application: "LinkApplication" = None
    button: "LinkButton" = None
    caption: str = None
    description: str = None
    id: str = None
    is_favorite: bool = None
    photo: "photos.Photo" = None
    preview_page: str = None
    preview_url: str = None
    product: "LinkProduct" = None
    rating: "LinkRating" = None
    title: str = None
    url: str = None


class LinkApplication(BaseModel):
    app_id: int = None
    store: "LinkApplicationStore" = None


class LinkApplicationStore(BaseModel):
    id: int = None
    name: str = None


class LinkButton(BaseModel):
    action: "LinkButtonAction" = None
    title: str = None


class LinkButtonAction(BaseModel):
    type: "LinkButtonActionType" = None
    url: str = None


class LinkButtonActionType(Enum):
    open_url = "open_url"
    join_group_and_open_url = "join_group_and_open_url"


class LinkProduct(BaseModel):
    price: "market.Price" = None
    merchant: str = None
    orders_count: int = None


class LinkRating(BaseModel):
    reviews_count: int = None
    stars: int = None


Link.update_forward_refs()
LinkApplication.update_forward_refs()
LinkApplicationStore.update_forward_refs()
LinkButton.update_forward_refs()
LinkButtonAction.update_forward_refs()
LinkProduct.update_forward_refs()
LinkRating.update_forward_refs()
