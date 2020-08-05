from . import (
    audio,
    docs,
    base,
    market,
    pages,
    photos,
    video,
    comment,
    events,
    polls,
    link,
)
import typing
from enum import Enum
from ..base import BaseModel


class AppPost(BaseModel):
    id: int = None
    name: str = None
    photo_130: str = None
    photo_604: str = None


class AttachedNote(BaseModel):
    comments: int = None
    date: int = None
    id: int = None
    owner_id: int = None
    read_comments: int = None
    title: str = None
    view_url: str = None

    def __hash__(self):
        return hash((self.owner_id, self.id))

    def __eq__(self, other):
        return self.owner_id == other.owner_id and self.id == other.id


class CommentAttachment(BaseModel):
    audio: "audio.Audio" = None
    doc: "docs.Doc" = None
    link: "link.Link" = None
    market: "market.MarketItem" = None
    market_market_album: "market.MarketAlbum" = None
    note: "AttachedNote" = None
    page: "pages.WikipageFull" = None
    photo: "photos.Photo" = None
    sticker: "base.Sticker" = None
    type: "CommentAttachmentType" = None
    video: "video.Video" = None


class CommentAttachmentType(Enum):
    photo = "photo"
    audio = "audio"
    video = "video"
    doc = "doc"
    link = "link"
    note = "note"
    page = "page"
    market_market_album = "market_market_album"
    market = "market"
    sticker = "sticker"


class Geo(BaseModel):
    coordinates: str = None
    place: "base.Place" = None
    showmap: int = None
    type: str = None


class Graffiti(BaseModel):
    id: int = None
    owner_id: int = None
    photo_200: str = None
    photo_586: str = None

    def __hash__(self):
        return hash((self.owner_id, self.id))

    def __eq__(self, other):
        return self.owner_id == other.owner_id and self.id == other.id


class PostSource(BaseModel):
    data: str = None
    platform: str = None
    type: "PostSourceType" = None
    url: str = None


class PostSourceType(Enum):
    vk = "vk"
    widget = "widget"
    api = "api"
    rss = "rss"
    sms = "sms"


class PostType(Enum):
    post = "post"
    copy = "copy"
    reply = "reply"
    postpone = "postpone"
    post_ads = "post_ads"
    suggest = "suggest"


class PostedPhoto(BaseModel):
    id: int = None
    owner_id: int = None
    photo_130: str = None
    photo_604: str = None

    def __hash__(self):
        return hash((self.owner_id, self.id))

    def __eq__(self, other):
        return self.owner_id == other.owner_id and self.id == other.id


class Views(BaseModel):
    count: int = None


class WallComment(BaseModel):
    attachments: typing.List[CommentAttachment] = None
    date: int = None
    from_id: int = None
    id: int = None
    likes: "base.LikesInfo" = None
    real_offset: int = None
    reply_to_comment: int = None
    reply_to_user: int = None
    text: str = None
    thread: "comment.Thread" = None
    post_id: int = None
    owner_id: int = None
    parents_stack: typing.List = None
    deleted: bool = None

    def __hash__(self):
        return hash((self.owner_id, self.id))

    def __eq__(self, other):
        return self.owner_id == other.owner_id and self.id == other.id


class Wallpost(BaseModel):
    access_key: str = None
    attachments: typing.List["WallpostAttachment"] = None
    date: int = None
    edited: int = None
    from_id: int = None
    geo: "Geo" = None
    id: int = None
    is_archived: bool = None
    is_favorite: bool = None
    likes: "base.LikesInfo" = None
    owner_id: int = None
    post_source: "PostSource" = None
    post_type: "PostType" = None
    reposts: "base.RepostsInfo" = None
    signer_id: int = None
    text: str = None
    views: "Views" = None

    def __hash__(self):
        return hash((self.owner_id, self.id))

    def __eq__(self, other):
        return self.owner_id == other.owner_id and self.id == other.id


class WallpostAttachment(BaseModel):
    access_key: str = None
    album: "photos.PhotoAlbum" = None
    app: "AppPost" = None
    audio: "audio.Audio" = None
    doc: "docs.Doc" = None
    event: "events.EventAttach" = None
    graffiti: "Graffiti" = None
    link: "link.Link" = None
    market: "market.MarketItem" = None
    market_album: "market.MarketAlbum" = None
    note: "AttachedNote" = None
    page: "pages.WikipageFull" = None
    photo: "photos.Photo" = None
    photos_list: typing.List = None
    poll: "polls.Poll" = None
    posted_photo: "PostedPhoto" = None
    type: "WallpostAttachmentType" = None
    video: "video.Video" = None


class WallpostAttachmentType(Enum):
    photo = "photo"
    posted_photo = "posted_photo"
    audio = "audio"
    video = "video"
    doc = "doc"
    link = "link"
    graffiti = "graffiti"
    note = "note"
    app = "app"
    poll = "poll"
    page = "page"
    album = "album"
    photos_list = "photos_list"
    market_market_album = "market_market_album"
    market = "market"
    event = "event"


class WallpostFull(Wallpost):
    copy_history: typing.List = None
    can_edit: "base.BoolInt" = None
    created_by: int = None
    can_delete: "base.BoolInt" = None
    can_pin: "base.BoolInt" = None
    is_pinned: int = None
    comments: "base.CommentsInfo" = None
    marked_as_ads: "base.BoolInt" = None


class WallpostToId(BaseModel):
    attachments: typing.List = None
    comments: "base.CommentsInfo" = None
    copy_owner_id: int = None
    copy_post_id: int = None
    date: int = None
    from_id: int = None
    geo: "Geo" = None
    id: int = None
    likes: "base.LikesInfo" = None
    post_id: int = None
    post_source: "PostSource" = None
    post_type: "PostType" = None
    reposts: "base.RepostsInfo" = None
    signer_id: int = None
    text: str = None
    to_id: int = None


AppPost.update_forward_refs()
AttachedNote.update_forward_refs()
CommentAttachment.update_forward_refs()
Geo.update_forward_refs()
Graffiti.update_forward_refs()
PostSource.update_forward_refs()
PostedPhoto.update_forward_refs()
Views.update_forward_refs()
WallComment.update_forward_refs()
Wallpost.update_forward_refs()
WallpostAttachment.update_forward_refs()
WallpostFull.update_forward_refs()
WallpostToId.update_forward_refs()
