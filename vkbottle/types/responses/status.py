from ..base import BaseModel
from vkbottle.types import objects

Get = objects.status.Status


class GetModel(BaseModel):
    response: Get = None
