from datetime import datetime
from typing import Union

from .base import BaseModel


class VKPayTransaction(BaseModel):
    from_id: int = None
    amount: Union[int, float] = None
    description: str = None
    date: int = None

    @property
    def date_time(self) -> datetime:
        return datetime.fromtimestamp(self.date)


class AppPayload(BaseModel):
    user_id: int = None
    app_id: int = None
    payload: str = None
    group_id: int = None


VKPayTransaction.update_forward_refs()
AppPayload.update_forward_refs()
