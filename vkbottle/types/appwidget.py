from .base import BaseModel

from typing import List


class Image(BaseModel):
    url: str = None
    width: int = None
    height: int = None


class AppWidgetImage(BaseModel):
    id: str = None
    type: str = None
    images: List[Image] = []
