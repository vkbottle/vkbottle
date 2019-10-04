from ..base import BaseModel


class Sticker(BaseModel):
    id: int = None
    product_id: int = None
    photo_64: str = None
    photo_128: str = None
    photo_256: str = None
    photo_352: str = None
    width: int = None
    height: int = None
