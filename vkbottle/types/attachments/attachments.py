from enum import Enum
from ..base import BaseModel
from .photo import Photo, PostedPhoto
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
from .sticker import Sticker
from .pretty_cards import PrettyCards
from .audio_msg import AudioMsg

import typing
from typing import Optional


# https://vk.com/dev/objects/attachments_w


class Attachments(str, Enum):
    not_attachments = []
    photo = Photo
    posted_photo = PostedPhoto
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
    sticker = Sticker
    pretty_cards = PrettyCards


class Attachment(BaseModel):
    type: str = None
    photo: Optional[Photo]
    posted_photo: Optional[PostedPhoto]
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
    sticker: Optional[Sticker]
    pretty_cards: Optional[PrettyCards]
    audio_message: Optional[AudioMsg]
