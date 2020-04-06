import typing
import enum
from ..base import BaseModel
from vkbottle.types import objects


class Restore(BaseModel):
    success: int = None
    sid: str = None


class RestoreModel(BaseModel):
    response: Restore = None
