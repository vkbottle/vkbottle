from . import base
import typing
from enum import Enum
from ..base import BaseModel
from vkbottle.types import objects


class City(base.Object):
    area: str = None
    region: str = None
    important: "base.BoolInt" = None


class Faculty(BaseModel):
    id: int = None
    title: str = None


class Region(BaseModel):
    id: int = None
    title: str = None


class School(BaseModel):
    id: int = None
    title: str = None


class Station(BaseModel):
    city_id: int = None
    color: str = None
    id: int = None
    name: str = None


class University(BaseModel):
    id: int = None
    title: str = None


