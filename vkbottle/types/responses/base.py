from ..base import BaseModel
from vkbottle.types import objects

GetUploadServer = objects.base.UploadServer


class GetUploadServerModel(BaseModel):
    response: GetUploadServer = None


Bool = objects.base.BoolInt


class BoolModel(BaseModel):
    response: Bool = None
