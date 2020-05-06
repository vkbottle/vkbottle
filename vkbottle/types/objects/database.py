from . import base
from ..base import BaseModel


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


City.update_forward_refs()
Faculty.update_forward_refs()
Region.update_forward_refs()
School.update_forward_refs()
Station.update_forward_refs()
University.update_forward_refs()
