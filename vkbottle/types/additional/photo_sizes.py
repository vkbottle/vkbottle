from ..base import BaseModel


class PhotoSizes(BaseModel):
    url: str = None
    width: int = None
    height: int = None
    type: str = None
