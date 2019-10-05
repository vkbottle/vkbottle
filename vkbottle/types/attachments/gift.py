from ..base import BaseModel


class Gift(BaseModel):
    id: int = None
    thumb_256: str = None
    thumb_96: str = None
    thumb_48: str = None
