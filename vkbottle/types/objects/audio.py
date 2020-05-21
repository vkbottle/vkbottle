from ..base import BaseModel
from typing import List


class AudioAds(BaseModel):
    content_id: str = None
    duration: str = None
    account_age_type: str = None


class AlbumThumb(BaseModel):
    width: int = None
    height: int = None
    photo_34: str = None
    photo_68: str = None
    photo_135: str = None
    photo_270: str = None
    photo_300: str = None
    photo_600: str = None
    photo_1200: str = None


class AudioAlbum(BaseModel):
    id: int = None
    title: str = None
    owner_id: int = None
    access_key: str = None
    thumb: AlbumThumb = None


class Artist(BaseModel):
    name: str = None
    domain: str = None
    id: str = None


class Audio(BaseModel):
    artist: str = None
    id: int = None
    owner_id: int = None
    title: str = None
    url: str = None
    duration: int = None
    access_key: str = None
    ads: AudioAds = None
    is_licensed: bool = None
    track_code: str = None
    date: int = None
    album_id: int = None
    album: AudioAlbum = None
    genre_id: int = None
    performer: str = None
    main_artists: List[Artist] = None


Audio.update_forward_refs()
