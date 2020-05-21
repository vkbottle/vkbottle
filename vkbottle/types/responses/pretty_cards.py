import typing
from ..base import BaseModel
from vkbottle.types import objects


class Get(BaseModel):
    count: int = None
    items: typing.List[objects.pretty_cards.PrettyCard] = None


class GetModel(BaseModel):
    response: Get = None


class Create(BaseModel):
    owner_id: int = None
    card_id: str = None


class CreateModel(BaseModel):
    response: Create = None


class Delete(BaseModel):
    owner_id: int = None
    card_id: str = None
    error: str = None


class DeleteModel(BaseModel):
    response: Delete = None


class Edit(BaseModel):
    owner_id: int = None
    card_id: str = None


class EditModel(BaseModel):
    response: Edit = None


GetById = typing.List[objects.pretty_cards.PrettyCard]


class GetByIdModel(BaseModel):
    response: GetById = None


GetUploadURL = typing.Dict


class GetUploadURLModel(BaseModel):
    response: GetUploadURL = None
