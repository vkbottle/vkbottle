from ..base import BaseModel

OkResponse = int


class OkResponseModel(BaseModel):
    response: int = None
