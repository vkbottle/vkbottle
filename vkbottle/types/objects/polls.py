import typing
from ..base import BaseModel


class Answer(BaseModel):
    id: int = None
    rate: float = None
    text: str = None
    votes: int = None


class Poll(BaseModel):
    anonymous: bool = None
    answer_id: int = None
    answers: typing.List[Answer] = None
    created: int = None
    id: int = None
    owner_id: int = None
    question: str = None
    votes: str = None

    def __hash__(self):
        return hash((self.owner_id, self.id))

    def __eq__(self, other):
        return self.owner_id == other.owner_id and self.id == other.id


class Voters(BaseModel):
    answer_id: int = None
    users: "VotersUsers" = None


class VotersUsers(BaseModel):
    count: int = None
    items: typing.List = None


Answer.update_forward_refs()
Poll.update_forward_refs()
Voters.update_forward_refs()
VotersUsers.update_forward_refs()
