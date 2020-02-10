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
from typing import List


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
    photos_list = List[int]
    market = Market
    market_album = MarketAlbum
    wall = WallPost
    wall_reply = WallComment
    sticker = Sticker
    gift = Gift


class Attachment(BaseModel):
    type: str = None
    photo: Photo = None
    video: Video = None
    audio: Audio = None
    doc: Document = None
    graffiti: Graffiti = None
    link: Link = None
    note: Note = None
    app: App = None
    poll: Poll = None
    page: Page = None
    album: Album = None
    photos_list: List[Photo] = []
    market: Market = None
    market_album: MarketAlbum = None
    wall: WallPost = None
    wall_reply: WallComment = None
    sticker: Sticker = None
    audio_message: AudioMsg = None
    gift: Gift = None
