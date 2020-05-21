import typing
from ..base import BaseModel
from vkbottle.types import objects


class Search(BaseModel):
    count: int = None
    items: typing.List[objects.docs.Doc] = None


class SearchModel(BaseModel):
    response: Search = None


class Add(BaseModel):
    id: int = None


class AddModel(BaseModel):
    response: Add = None


GetById = typing.List[objects.docs.Doc]


class GetByIdModel(BaseModel):
    response: GetById = None


class DocType(BaseModel):
    id: int = None
    name: str = None
    count: int = None


class GetTypes(BaseModel):
    count: int = None
    items: typing.List[DocType] = None


class GetTypesModel(BaseModel):
    response: GetTypes = None


class Get(BaseModel):
    count: int = None
    items: typing.List[objects.docs.Doc] = None


class GetModel(BaseModel):
    response: Get = None


class Save(BaseModel):
    type: objects.docs.DocAttachmentType = None
    audio_message: objects.messages.AudioMessage = None
    doc: objects.docs.Doc = None
    graffiti: objects.messages.Graffiti = None


class SaveModel(BaseModel):
    response: Save = None
