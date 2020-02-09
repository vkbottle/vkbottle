from enum import Enum
from ..base import BaseModel
from .photo import Photo
from .video import Video
from .audio import Audio
from .document import Document
from .graffiti import Graffiti
from .link import Link
from .note import Note
from .app import App
from .poll import Poll
from .page import Page
from .album import Album
from .market import Market
from .market_album import MarketAlbum
from ..wall_post import WallPost
from ..wall_comment import WallComment
from .sticker import Sticker
from .audio_msg import AudioMsg
from .gift import Gift

import typing
from typing import Optional


# https://vk.com/dev/objects/attachments_m


class Attachments(str, Enum):
    not_attachments = []
    photo = Photo
    video = Video
    audio = Audio
    document = Document
    graffiti = Graffiti
    link = Link
    note = Note
    app = App
    poll = Poll
    page = Page
    album = Album
    photos_list = typing.List[int]
    market = Market
    market_album = MarketAlbum
    wall = WallPost
    wall_reply = WallComment
    sticker = Sticker
    gift = Gift


class Attachment(BaseModel):
    type: str = None
    photo: Optional[Photo]
    video: Optional[Video]
    audio: Optional[Audio]
    doc: Optional[Document]
    graffiti: Optional[Graffiti]
    link: Optional[Link]
    note: Optional[Note]
    app: Optional[App]
    poll: Optional[Poll]
    page: Optional[Page]
    album: Optional[Album]
    photos_list: Optional[typing.List[Photo]]
    market: Optional[Market]
    market_album: Optional[MarketAlbum]
    wall: Optional[WallPost]
    wall_reply: Optional[WallComment]
    sticker: Optional[Sticker]
    audio_message: Optional[AudioMsg]
    gift: Optional[Gift]
