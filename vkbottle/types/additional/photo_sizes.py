from ..base import BaseModel


class PhotoSizes(BaseModel):
    src: str = None
    width: int = None
    height: int = None
    type: str = None
