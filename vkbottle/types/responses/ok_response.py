from ..base import BaseModel
import typing

OkResponse = int


class OkResponseModel(BaseModel):
    response: typing.Union[int, dict] = None
