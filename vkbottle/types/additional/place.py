from ..base import BaseModel

import typing


class Place(BaseModel):
    id: int = None
    title: str = None
    latitude: typing.Union[int, float] = None
    longitude: typing.Union[int, float] = None
    type: str = None
    country: int = None
    city: int = None
    address: str = None


class GeoPlace(BaseModel):
    id: int = None
    title: str = None
    latitude: int = None
    longitude: int = None
    created: int = None
    icon: str = None
    country: str = None
    city: str = None
    type: int = None
    group_id: int = None
    group_photo: str = None
    checkins: int = None
    updated: int = None
    address: int = None
