from enum import IntEnum
from ..base import BaseModel


class Gift(BaseModel):
    date: int = None
    from_id: int = None
    gift: "Layout" = None
    gift_hash: str = None
    id: int = None
    message: str = None
    privacy: "GiftPrivacy" = None

    def __hash__(self):
        return hash((self.from_id, self.id))

    def __eq__(self, other):
        return self.from_id == other.from_id and self.id == other.id


class GiftPrivacy(IntEnum):
    visible_name_and_message = 0
    visible_name = 1
    visible_only_owner = 2


class Layout(BaseModel):
    id: int = None
    thumb_256: str = None
    thumb_48: str = None
    thumb_96: str = None

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return self.id == other.id


Gift.update_forward_refs()
Layout.update_forward_refs()
