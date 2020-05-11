from ..base import BaseModel


class Value(BaseModel):
    key: str = None
    value: str = None


Value.update_forward_refs()
