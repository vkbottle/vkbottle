from .others import SimpleResponse
from ..base import BaseModel

from ..attachments import Document

from typing import List


class Add(SimpleResponse):
    pass


class Delete(SimpleResponse):
    pass


class Edit(SimpleResponse):
    pass


class GetResponse(BaseModel):
    count: int = None
    items: List[Document] = []


class Get(BaseModel):
    response: GetResponse = None


class GetById(BaseModel):
    response: List[Document] = []


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
    items: List[GetTypesItems] = []


class GetTypes(BaseModel):
    response: GetTypesResponse = None


class GetUploadServer(BaseModel):
    response: GetMessagesUploadServerResponse = None


class GetWallUploadServer(BaseModel):
    response: GetMessagesUploadServerResponse = None


class Save(BaseModel):
    response: List[Document] = []


class SearchResponse(BaseModel):
    count: int = None
    items: List[Document] = []


class Search(BaseModel):
    response: SearchResponse = None
