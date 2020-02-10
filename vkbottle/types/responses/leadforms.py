from .others import SimpleResponse
from ..base import BaseModel

from typing import Any, List


class CreateResponse(BaseModel):
    form_id: int = None
    url: str = None


class Create(BaseModel):
    response: CreateResponse = None


class Delete(SimpleResponse):
    pass


class Get(SimpleResponse):
    pass


class GetLeads(BaseModel):
    response: Any = None


class GetUploadURL(BaseModel):
    response: str = None


class List(BaseModel):
    response: List = []


class Update(SimpleResponse):
    pass
