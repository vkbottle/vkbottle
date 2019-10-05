from .others import SimpleResponse
from ..base import BaseModel

from ..attachments import Document

import typing


class Add(SimpleResponse):
    pass


class Delete(SimpleResponse):
    pass


class Edit(SimpleResponse):
    pass


class GetResponse(BaseModel):
    count: int = None
    items: typing.List[Document] = None


class Get(BaseModel):
    response: GetResponse = None


class GetById(BaseModel):
    response: typing.List[Document] = None


class GetMessagesUploadServerResponse(BaseModel):
    upload_url: str = None


class GetMessagesUploadServer(BaseModel):
    response: GetMessagesUploadServerResponse = None


class GetTypesItems(BaseModel):
    id: int = None
    name: str = None
    count: int = None


class GetTypesResponse(BaseModel):
    count: int = None
    items: typing.List[GetTypesItems] = None


class GetTypes(BaseModel):
    response: GetTypesResponse = None


class GetUploadServer(BaseModel):
    response: GetMessagesUploadServerResponse = None


class GetWallUploadServer(BaseModel):
    response: GetMessagesUploadServerResponse = None


class Save(BaseModel):
    response: typing.List[Document] = None


class SearchResponse(BaseModel):
    count: int = None
    items: typing.List[Document] = None


class Search(BaseModel):
    response: SearchResponse = None
