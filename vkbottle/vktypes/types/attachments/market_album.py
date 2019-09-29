from ..base import BaseModel
from ..attachments import Photo

# https://vk.com/dev/objects/market_album


class MarketAlbum(BaseModel):
    id: int = None
    owner_id: int = None
    title: str = None
    photo: Photo = None
    count: int = None
    updated_time: int = None
