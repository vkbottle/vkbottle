from .base import BaseModel
import typing


class Image(BaseModel):
    url: str = None
    width: int = None
    height: int = None


class AppWidgetImage(BaseModel):
    id: str = None
    type: str = None
    images: typing.List[Image] = None
