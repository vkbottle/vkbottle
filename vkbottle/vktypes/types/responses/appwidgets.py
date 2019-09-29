from .others import SimpleResponse
from ..base import BaseModel

from ..appwidget import AppWidgetImage

import typing


class GetAppImageUploadServerResponse(BaseModel):
    upload_url: str = None


class GetAppImageUploadServer(BaseModel):
    response: GetAppImageUploadServerResponse = None


class GetAppImagesResponse(BaseModel):
    count: int = None
    items: typing.List[AppWidgetImage] = None


class GetAppImages(BaseModel):
    response: GetAppImagesResponse = None


class GetGroupImageUploadServer(GetAppImageUploadServer):
    pass


class GetGroupImages(GetAppImages):
    pass


class GetImagesById(BaseModel):
    response: AppWidgetImage = None


class SaveAppImage(GetImagesById):
    pass


class SaveGroupImage(SaveAppImage):
    pass


class Update(SimpleResponse):
    pass
