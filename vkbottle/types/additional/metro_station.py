from ..base import BaseModel


class MetroStation(BaseModel):
    id: int = None
    name: str = None
    color: str = None
    city_id: int = None
