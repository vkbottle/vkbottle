from ..base import BaseModel
from ..additional import PhotoSizes

import typing

# https://vk.com/dev/objects/photo


class Photo(BaseModel):
    id: int = None
    album_id: int = None
    owner_id: int = None
    user_id: int = None
    text: str = None
    date: int = None
    sizes: typing.List[PhotoSizes] = []
    width: int = None
    height: int = None


class PostedPhoto(BaseModel):
    id: int = None
    owner_id: int = None
    photo_130: str = None
    photo_604: str = None


class CropPhotoCrop(BaseModel):
    x: int = None
    y: int = None
    x2: int = None
    y2: int = None


class CropPhoto(BaseModel):
    photo: Photo = None
    crop: CropPhotoCrop = None
    rect: CropPhotoCrop = None
