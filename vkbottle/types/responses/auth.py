from ..base import BaseModel


class Restore(BaseModel):
    success: int = None
    sid: str = None


class RestoreModel(BaseModel):
    response: Restore = None
