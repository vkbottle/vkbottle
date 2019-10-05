from ..base import BaseModel
from ..additional import AudioGenres

import typing


# https://vk.com/dev/objects/audio


class Audio(BaseModel):
    id: int = None
    owner_id: int = None
    artist: str = None
    title: str = None
    duration: int = None
    url: str = None
    lyrics_id: int = None
    album_id: int = None
    genre_id: AudioGenres = None
    date: int = None
    no_search: int = 0
