from ..base import BaseModel
from ..attachments import Photo

from typing import Any


class Link(BaseModel):
    url: str = None
    title: str = None
    caption: str = None
    description: str = None
    photo: Photo = None
    is_external: int = None
    product: Any = None
    button: Any = None
    preview_page: str = None
    preview_url: str = None
