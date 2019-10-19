from ..base import BaseModel
from ..attachments import Photo
from ..additional import PhotoSizes

from typing import List
import typing


# https://vk.com/dev/objects/poll


class PollAnswer(BaseModel):
    id: int = None
    text: str = None
    votes: int = None
    rate: typing.Union[int, float] = None


class PollBackgroundPoint(BaseModel):
    position: typing.Union[int, float] = None
    color: str = None


class PollBackground(BaseModel):
    id: int = None
    type: str = None
    angle: int = None
    color: str = None
    width: int = None
    height: int = None
    images: List[PhotoSizes] = None
    points: List[PollBackgroundPoint]


class PollFriends(BaseModel):
    id: int = None


class Poll(BaseModel):
    id: int = None
    owner_id: int = None
    created: int = None
    question: str = None
    votes: int = None
    answers: List[PollAnswer] = None
    anonymous: bool = None
    multiple: bool = None
    answer_ids: List[int] = None
    end_date: int = None
    closed: bool = None
    is_board: bool = None
    can_edit: bool = None
    can_vote: bool = None
    can_report: bool = None
    can_share: bool = None
    author_id: int = None
    photo: Photo = None
    background: PollBackground = None
    friends: List[PollFriends] = None
