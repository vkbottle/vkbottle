from ..base import BaseModel


class PostSource(BaseModel):
    type: str = None
    platform: str = None
    data: str = None
    url: str = None
