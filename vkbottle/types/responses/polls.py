import typing
from ..base import BaseModel
from vkbottle.types import objects

GetVoters = typing.List[objects.polls.Voters]


class GetVotersModel(BaseModel):
    response: GetVoters = None


AddVote = objects.base.BoolInt


class AddVoteModel(BaseModel):
    response: AddVote = None


Create = objects.polls.Poll


class CreateModel(BaseModel):
    response: Create = None


DeleteVote = objects.base.BoolInt


class DeleteVoteModel(BaseModel):
    response: DeleteVote = None


GetById = objects.polls.Poll


class GetByIdModel(BaseModel):
    response: GetById = None
