import typing
import enum
from ..base import BaseModel
from vkbottle.types import objects


class GetServerUrl(BaseModel):
    endpoint: str = None
    key: str = None


class GetServerUrlModel(BaseModel):
    response: GetServerUrl = None
