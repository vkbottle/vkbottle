from ..base import BaseModel


class Note(BaseModel):
    id: int = None
    user_id: int = None
    title: str = None
    text: str = None
    date: int = None
    comments: int = None
    read_comments: int = None
