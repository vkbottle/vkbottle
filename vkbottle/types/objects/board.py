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


class Topic(BaseModel):
    comments: int = None
    created: int = None
    created_by: int = None
    id: int = None
    is_closed: "base.BoolInt" = None
    is_fixed: "base.BoolInt" = None
    title: str = None
    updated: int = None
    updated_by: int = None

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return self.id == other.id


class TopicComment(BaseModel):
    attachments: typing.List["TopicAttachment"] = None
    date: int = None
    from_id: int = None
    id: int = None
    real_offset: int = None
    text: str = None
    can_edit: "base.BoolInt" = None


class TopicPoll(BaseModel):
    answer_id: int = None
    answers: typing.List = None
    created: int = None
    is_closed: "base.BoolInt" = None
    owner_id: int = None
    poll_id: int = None
    question: str = None
    votes: str = None


class TopicAttachment(BaseModel):
    type: "TopicAttachmentType" = None
    audio: "audio.Audio" = None
    doc: "docs.Doc" = None
    link: "link.Link" = None
    market: "market.MarketItem" = None
    market_market_album: "market.MarketAlbum" = None
    page: "pages.WikipageFull" = None
    photo: "photos.Photo" = None
    sticker: "base.Sticker" = None
    graffiti: "base.Graffiti" = None
    video: "video.Video" = None


class TopicAttachmentType(Enum):
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
    graffiti = "graffiti"


TopicAttachment.update_forward_refs()
Topic.update_forward_refs()
TopicComment.update_forward_refs()
TopicPoll.update_forward_refs()
