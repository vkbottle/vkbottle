from .others import SimpleResponse
from ..base import BaseModel


import typing


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
    response: typing.Any = None


class GetUploadURL(BaseModel):
    response: str = None


class List(BaseModel):
    response: typing.List = None


class Update(SimpleResponse):
    pass
