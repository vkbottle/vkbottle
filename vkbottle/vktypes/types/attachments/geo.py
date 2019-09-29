from ..base import BaseModel
from ..additional import GeoPlace


class Geo(BaseModel):
    type: str = None
    coordinates: str = None
    place: GeoPlace = None
