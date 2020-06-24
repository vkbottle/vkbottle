from . import wall, market, video, groups, users, link
import typing
from enum import Enum
from ..base import BaseModel


class Bookmark(BaseModel):
    added_date: int = None
    link: "link.Link" = None
    post: "wall.WallpostFull" = None
    product: "market.MarketItem" = None
    seen: bool = None
    tags: typing.List = None
    type: "BookmarkType" = None
    video: "video.Video" = None


class BookmarkType(Enum):
    post = "post"
    video = "video"
    product = "product"
    article = "article"
    link = "link"


class Page(BaseModel):
    description: str = None
    group: "groups.GroupFull" = None
    tags: typing.List = None
    type: "PageType" = None
    updated_date: int = None
    user: "users.UserFull" = None


class PageType(Enum):
    user = "user"
    group = "group"
    hints = "hints"


class Tag(BaseModel):
    id: int = None
    name: str = None

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return self.id == other.id


Bookmark.update_forward_refs()
Page.update_forward_refs()
Tag.update_forward_refs()
