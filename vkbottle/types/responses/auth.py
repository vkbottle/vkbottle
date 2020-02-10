from .others import SimpleResponse
from ..base import BaseModel

from typing import Any


class CheckPhone(SimpleResponse):
    pass


class RestoreResponse(BaseModel):
    success: int = None
    sid: Any = None
