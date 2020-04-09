import typing
from enum import Enum
from ..base import BaseModel
from vkbottle.types import objects


class Value(BaseModel):
    key: str = None
    value: str = None


Value.update_forward_refs()
