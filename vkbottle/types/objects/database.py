from . import base
from ..base import BaseModel


class City(base.Object):
    area: str = None
    region: str = None
    important: "base.BoolInt" = None


class Faculty(BaseModel):
    id: int = None
    title: str = None

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return self.id == other.id


class Region(BaseModel):
    id: int = None
    title: str = None

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return self.id == other.id


class School(BaseModel):
    id: int = None
    title: str = None

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return self.id == other.id


class Station(BaseModel):
    city_id: int = None
    color: str = None
    id: int = None
    name: str = None

    def __hash__(self):
        return hash((self.city_id, self.id))

    def __eq__(self, other):
        return self.city_id == other.city_id and self.id == other.id


class University(BaseModel):
    id: int = None
    title: str = None

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return self.id == other.id


City.update_forward_refs()
Faculty.update_forward_refs()
Region.update_forward_refs()
School.update_forward_refs()
Station.update_forward_refs()
University.update_forward_refs()
