from ..base import BaseModel

import typing


# https://vk.com/dev/objects/video


class Video(BaseModel):
    id: int = None
    owner_id: int = None
    title: str = None
    description: str = None
    duration: int = None
    photo_130: str = None
    photo_320: str = None
    photo_640: str = None
    photo_800: str = None
    date: int = None
    adding_date: int = None
    views: int = None
    comments: int = None
    player: str = None
    access_key: str = None
    processing: int = None
    live: int = None
    upcoming: int = None
    is_favorite: bool = None
