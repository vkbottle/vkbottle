from . import base
from ..base import BaseModel


class Note(BaseModel):
    read_comments: int = None
    can_comment: "base.BoolInt" = None
    comments: int = None
    date: int = None
    id: int = None
    owner_id: int = None
    text: str = None
    text_wiki: str = None
    title: str = None
    view_url: str = None

    def __hash__(self):
        return hash((self.owner_id, self.id))

    def __eq__(self, other):
        return self.owner_id == other.owner_id and self.id == other.id


class NoteComment(BaseModel):
    date: int = None
    id: int = None
    message: str = None
    nid: int = None
    oid: int = None
    reply_to: int = None
    uid: int = None


Note.update_forward_refs()
NoteComment.update_forward_refs()
