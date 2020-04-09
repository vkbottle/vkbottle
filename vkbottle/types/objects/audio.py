import typing
from enum import Enum
from ..base import BaseModel
from vkbottle.types import objects


class Audio(BaseModel):
    artist: str = None
    id: int = None
    title: str = None
    url: str = None
    duration: int = None
    date: int = None
    album_id: int = None
    genre_id: int = None
    performer: str = None


Audio.update_forward_refs()
