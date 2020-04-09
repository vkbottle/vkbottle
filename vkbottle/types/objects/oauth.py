import typing
from enum import Enum
from ..base import BaseModel
from vkbottle.types import objects


class Error(BaseModel):
    error: str = None
    error_description: str = None
    redirect_uri: str = None


Error.update_forward_refs()
