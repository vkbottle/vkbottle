from ..base import BaseModel


class Like(BaseModel):
    user_likes: int = None
    count: int = None
    can_like: int = None
    can_publish: int = None
