from ..base import BaseModel
from typing import List

class Event(BaseModel):
    id: int = None
    time: int = None
    member_status: int = None
    is_favorite: bool = None
    address: str = None
    text: str = None
    button_text: str = None
    friends: List[int] = []
