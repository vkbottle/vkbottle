from .others import SimpleResponse
from ..base import BaseModel


import typing


class CheckPhone(SimpleResponse):
    pass


class RestoreResponse(BaseModel):
    success: int = None
    sid: typing.Any = None
