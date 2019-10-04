from ..base import BaseModel


class Repost(BaseModel):
    count: int = None
    user_reposted: int = None
