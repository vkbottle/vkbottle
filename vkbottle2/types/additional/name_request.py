from ..base import BaseModel
from enum import Enum

# Part of https://vk.com/dev/account.getProfileInfo?params[v]=5.101


class NameRequestStatus(Enum):
    processing = "processing"
    declined = "declined"


class NameRequest(BaseModel):
    id: int = None
    status: NameRequestStatus = None
    first_name: str = None
    last_name: str
